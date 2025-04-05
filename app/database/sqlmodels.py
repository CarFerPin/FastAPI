from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.dbhandler import Base


class Item(Base):
    """
    SQLAlchemy model for the items table.

    Represents an electronic product.

    Attributes:
        id (UUID): The unique identifier for the item.
        name (str): The name of the item.
        description (str): A description of the item.
        price (float): The price of the item.
        available (bool): Indicates whether the item is available.
    """
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True)


class User(Base):
    """
    SQLAlchemy model for the users table.

    Represents a user in the system.

    Attributes:
        id (UUID): The unique identifier for the user.
        username (str): The username of the user.
        full_name (str): The full name of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        disabled (bool): Indicates whether the user is disabled.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)