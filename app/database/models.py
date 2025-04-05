from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import Optional


class ItemBase(BaseModel):
    """
    Base model for an electronic product.

    Attributes:
        name (str): The name of the product.
        description (Optional[str]): A description of the product.
        price (float): The price of the product (must be greater than 0).
        available (bool): Indicates whether the product is available.
    """
    name: str = Field(..., title="Product Name", max_length=100)
    description: Optional[str] = Field(None, title="Product Description", max_length=500)
    price: float = Field(..., gt=0, title="Product Price")
    available: bool = Field(..., title="Product Availability")


class ItemCreate(ItemBase):
    """
    Model for creating a new product.

    Inherits:
        ItemBase: Includes all fields from the base model.
    """
    pass


class Item(ItemBase):
    """
    Model for representing a product with a unique identifier.

    Attributes:
        id (UUID): The unique identifier for the product.
    """
    id: UUID = Field(default_factory=uuid4, title="Unique Product Identifier")

    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    """
    Model for partial updates to a product.

    All fields are optional.

    Attributes:
        name (Optional[str]): The updated name of the product.
        description (Optional[str]): The updated description of the product.
        price (Optional[float]): The updated price of the product.
        available (Optional[bool]): The updated availability status of the product.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Smartphone Pro",
                "description": "Smartphone with AMOLED display and 5G support",
                "price": 999.99,
                "available": True,
            }
        }
    )


class UserBase(BaseModel):
    """
    Base model for a user.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        full_name (Optional[str]): The full name of the user.
        disabled (Optional[bool]): Indicates whether the user is disabled.
    """
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserCreate(UserBase):
    """
    Model for creating a new user.

    Inherits:
        UserBase: Includes all fields from the base model.

    Attributes:
        password (str): The password for the new user.
    """
    password: str


class UserUpdate(BaseModel):
    """
    Model for partial updates to a user.

    All fields are optional.

    Attributes:
        full_name (Optional[str]): The updated full name of the user.
        email (Optional[str]): The updated email address of the user.
        disabled (Optional[bool]): The updated disabled status of the user.
    """
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(UserBase):
    """
    Model for a user stored in the database.

    Inherits:
        UserBase: Includes all fields from the base model.

    Attributes:
        id (UUID): The unique identifier for the user.
        hashed_password (str): The hashed password of the user.
    """
    id: UUID
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)