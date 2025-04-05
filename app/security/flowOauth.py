from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.dbhandler import get_db
from app.database.sqlmodels import User as SQLUser

# Authentication configuration
SECRET_KEY = "71352f5d937040fd91d29fa00379f4f5f2926bbd4ea981172ff3f71d460a8639"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Data models
class Token(BaseModel):
    """
    Model for an access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token (e.g., "Bearer").
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for token data.

    Attributes:
        username (Optional[str]): The username extracted from the token.
    """
    username: Optional[str] = None


class User(BaseModel):
    """
    Model for a user.

    Attributes:
        username (str): The username of the user.
        email (Optional[str]): The email address of the user.
        full_name (Optional[str]): The full name of the user.
        disabled (Optional[bool]): Indicates whether the user is disabled.
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """
    Model for a user stored in the database.

    Inherits:
        User: Includes all fields from the base user model.

    Attributes:
        hashed_password (str): The hashed password of the user.
    """
    hashed_password: str


# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def get_user_by_username(db: Session, username: str) -> Optional[SQLUser]:
    """
    Retrieve a user by their username from the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[SQLUser]: The user object if found, None otherwise.
    """
    return db.query(SQLUser).filter(SQLUser.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[SQLUser]:
    """
    Authenticate a user by their username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The plain text password of the user.

    Returns:
        Optional[SQLUser]: The authenticated user object if valid, None otherwise.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The expiration time delta.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The access token.
        db (Session): The database session.

    Returns:
        SQLUser: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Retrieve the current active user.

    Args:
        token (str): The access token.
        db (Session): The database session.

    Returns:
        SQLUser: The authenticated and active user.

    Raises:
        HTTPException: If the user is inactive.
    """
    user = await get_current_user(token, db)
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user




