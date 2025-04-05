from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.users import create_user, get_user_by_username
from app.database.models import UserCreate, UserInDB
from app.database.dbhandler import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users Management"]
)

@router.post("/", response_model=UserInDB)
async def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        UserInDB: The created user.

    Raises:
        HTTPException: If the username is already registered.
    """
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return create_user(db, user)

@router.get("/{username}", response_model=UserInDB)
async def get_user_by_username_endpoint(
    username: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserInDB: The user with the specified username.

    Raises:
        HTTPException: If the user is not found.
    """
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user