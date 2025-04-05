from fastapi import FastAPI, Depends, HTTPException, status, Body
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.security.flowOauth import (
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.database.dbhandler import SessionLocal, Base, engine
from enum import Enum
from app.core.middlewares import add_middlewares
from app.database.dbhandler import get_db
from app.core.logging_config import log_request_response, log_error
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers.predict_sales import router as predict_sales_router
from app.routers.items import router as items_router
from app.routers.users import router as users_router

class Availability(str, Enum):
    """
    Enum to represent item availability status.

    Attributes:
        available (str): Indicates the item is available.
        not_available (str): Indicates the item is not available.
    """
    available = "available"
    not_available = "not_available"

# Create database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI application
app = FastAPI()

# Add middlewares
add_middlewares(app)

# Add logging middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_response)

# Include routers
app.include_router(items_router)
app.include_router(users_router)
app.include_router(predict_sales_router)

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Endpoint to obtain an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        db (Session): The database session.

    Returns:
        Token: The generated access token.

    Raises:
        HTTPException: If the username or password is incorrect or if an internal error occurs.
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        log_error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

@app.on_event("shutdown")
async def shutdown():
    """
    Event triggered when the application shuts down.

    Closes all active database connections.
    """
    SessionLocal.close_all()


