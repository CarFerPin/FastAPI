from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.crud.items import (
    create_item,
    get_items,
    get_item_by_id,
    update_item_by_id,
    patch_item_by_id,
    delete_item_by_id,
)
from app.database.models import ItemCreate, ItemUpdate, Item
from app.database.dbhandler import get_db
from app.security.flowOauth import get_current_active_user

router = APIRouter(
    prefix="/items",
    tags=["Items Management"]
)

@router.post("/", response_model=Item)
async def create_item_endpoint(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Create a new item.

    Args:
        item (ItemCreate): The item data to create.
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        Item: The created item.
    """
    return create_item(db, item)

@router.get("/", response_model=List[Item])
async def get_items_endpoint(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Retrieve all items.

    Args:
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        List[Item]: A list of all items.
    """
    return get_items(db)

@router.get("/{item_id}", response_model=Item)
async def get_item_by_id_endpoint(
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Retrieve an item by its ID.

    Args:
        item_id (UUID): The ID of the item to retrieve.
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        Item: The item with the specified ID.

    Raises:
        HTTPException: If the item is not found.
    """
    try:
        return get_item_by_id(db, item_id)
    except HTTPException as e:
        raise e

@router.put("/{item_id}", response_model=Item)
async def update_item_by_id_endpoint(
    item_id: UUID,
    updated_item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Update an item by its ID.

    Args:
        item_id (UUID): The ID of the item to update.
        updated_item (ItemUpdate): The updated item data.
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        Item: The updated item.
    """
    return update_item_by_id(db, item_id, updated_item)

@router.patch("/{item_id}", response_model=Item)
async def patch_item_by_id_endpoint(
    item_id: UUID,
    partial_update: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Partially update an item by its ID.

    Args:
        item_id (UUID): The ID of the item to update.
        partial_update (dict): The partial update data.
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        Item: The partially updated item.
    """
    return patch_item_by_id(db, item_id, partial_update)

@router.delete("/{item_id}", response_model=dict)
async def delete_item_by_id_endpoint(
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user),
):
    """
    Delete an item by its ID.

    Args:
        item_id (UUID): The ID of the item to delete.
        db (Session): The database session.
        current_user (dict): The currently authenticated user.

    Returns:
        dict: A message indicating the item was deleted.
    """
    return delete_item_by_id(db, item_id)