from sqlalchemy.orm import Session
from app.database.dbhandler import SessionLocal
from app.crud.users import create_user
from app.database.models import UserCreate

def main():
    """
    Create a new user in the database.

    This script initializes a database session, creates a new user with predefined
    attributes, and saves the user to the database.

    Returns:
        None
    """
    db: Session = SessionLocal()
    user = UserCreate(
        username="johndoe",
        email="johndoe@example.com",
        full_name="John Doe",
        password="secret",  # Plain text password
    )
    db_user = create_user(db, user)
    print(f"User created: {db_user.username}")

if __name__ == "__main__":
    main()