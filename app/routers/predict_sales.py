from fastapi import APIRouter, HTTPException, Depends, Body, status
from typing import Annotated
from app.ml.ml_model import get_sales_prediction  # Import from ml_model
from app.security.flowOauth import get_current_active_user

router = APIRouter(
    prefix="/predict-sales",
    tags=["Sales Prediction"]
)

@router.post("/", summary="Predict sales based on input features")
async def predict_sales_endpoint(
    features: Annotated[list[float], Body(..., examples=[50.0])],
    current_user: dict = Depends(get_current_active_user),
):
    """
    Predict sales based on input features.

    Args:
        features (list[float]): A list of numerical feature values (e.g., marketing spend).
        current_user (dict): The currently authenticated user.

    Returns:
        dict: A dictionary containing the input features and the predicted sales value.

    Raises:
        HTTPException: If the input features are invalid or a prediction error occurs.
    """
    try:
        prediction = get_sales_prediction(features)
        return {"features": features, "predicted_sales": prediction}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )