from sqlalchemy.orm import Session
from uuid import UUID
from app.database.models import UserCreate, UserUpdate
from app.database.sqlmodels import User as SQLUser
from passlib.context import CryptContext
from fastapi import HTTPException

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        SQLUser: The created user.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = SQLUser(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        disabled=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[SQLUser]: A list of all users.
    """
    return db.query(SQLUser).all()

def get_user_by_id(db: Session, user_id: UUID):
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (UUID): The ID of the user to retrieve.

    Returns:
        SQLUser: The user with the specified ID.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )
    return db_user

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        SQLUser: The user with the specified username.
    """
    return db.query(SQLUser).filter(SQLUser.username == username).first()

def update_user_by_id(db: Session, user_id: UUID, updated_user: UserUpdate):
    """
    Update a user by their ID.

    Args:
        db (Session): The database session.
        user_id (UUID): The ID of the user to update.
        updated_user (UserUpdate): The updated user data.

    Returns:
        SQLUser: The updated user.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )
    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def patch_user_by_id(db: Session, user_id: UUID, partial_update: dict):
    """
    Partially update a user by their ID.

    Args:
        db (Session): The database session.
        user_id (UUID): The ID of the user to update.
        partial_update (dict): The partial update data.

    Returns:
        SQLUser: The partially updated user.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )
    for key, value in partial_update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_id(db: Session, user_id: UUID):
    """
    Delete a user by their ID.

    Args:
        db (Session): The database session.
        user_id (UUID): The ID of the user to delete.

    Returns:
        dict: A message indicating the user was deleted.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}