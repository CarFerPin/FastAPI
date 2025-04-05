from sqlalchemy.orm import Session
from uuid import UUID
from app.database.models import ItemCreate, ItemUpdate
from app.database.sqlmodels import Item as SQLItem
from fastapi import HTTPException, status

def create_item(db: Session, item: ItemCreate):
    """
    Create a new item in the database.

    Args:
        db (Session): The database session.
        item (ItemCreate): The item data to create.

    Returns:
        SQLItem: The created item.
    """
    db_item = SQLItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session):
    """
    Retrieve all items from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[SQLItem]: A list of all items.
    """
    return db.query(SQLItem).all()

def get_item_by_id(db: Session, item_id: UUID):
    """
    Retrieve an item by its ID.

    Args:
        db (Session): The database session.
        item_id (UUID): The ID of the item to retrieve.

    Returns:
        SQLItem: The item with the specified ID.

    Raises:
        HTTPException: If the item is not found.
    """
    db_item = db.query(SQLItem).filter(SQLItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return db_item

def update_item_by_id(db: Session, item_id: UUID, updated_item: ItemUpdate):
    """
    Update an item by its ID.

    Args:
        db (Session): The database session.
        item_id (UUID): The ID of the item to update.
        updated_item (ItemUpdate): The updated item data.

    Returns:
        SQLItem: The updated item.

    Raises:
        HTTPException: If the item is not found.
    """
    db_item = db.query(SQLItem).filter(SQLItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    for key, value in updated_item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def patch_item_by_id(db: Session, item_id: UUID, partial_update: dict):
    """
    Partially update an item by its ID.

    Args:
        db (Session): The database session.
        item_id (UUID): The ID of the item to update.
        partial_update (dict): The partial update data.

    Returns:
        SQLItem: The partially updated item.

    Raises:
        HTTPException: If the item is not found.
    """
    db_item = db.query(SQLItem).filter(SQLItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    for key, value in partial_update.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item_by_id(db: Session, item_id: UUID):
    """
    Delete an item by its ID.

    Args:
        db (Session): The database session.
        item_id (UUID): The ID of the item to delete.

    Returns:
        dict: A message indicating the item was deleted.

    Raises:
        HTTPException: If the item is not found.
    """
    db_item = db.query(SQLItem).filter(SQLItem.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    db.delete(db_item)
    db.commit()
    return {"message": f"Item with ID {item_id} has been deleted"}