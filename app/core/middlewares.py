from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.items import router as items_router  # Import the items router
from app.routers.users import router as users_router  # Import the users router
from app.security.flowOauth import app as auth_app  # Import the authentication app

def add_middlewares(app: FastAPI):
    """
    Add middlewares to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Define allowed origins for CORS
    allowed_origins = [
        "http://localhost:7000",  # Allow access only from localhost on port 7000
    ]

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,  # Allowed domains
        allow_credentials=True,  # Allow sending cookies and credentials
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # Allowed HTTP methods
        allow_headers=["*"],  # Allowed headers
    )

def add_routers(app: FastAPI):
    """
    Register routers for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Mount the authentication app under the /auth prefix
    app.mount("/auth", auth_app)

    # Include the items and users routers
    app.include_router(items_router, prefix="/items", tags=["Items Management"])
    app.include_router(users_router, prefix="/users", tags=["Users Management"])

