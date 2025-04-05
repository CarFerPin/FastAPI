import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import joblib
import os

# Path to save the trained model
MODEL_PATH = "sales_prediction_model.pkl"


def train_model():
    """
    Train a simple regression model using synthetic data.

    This function generates synthetic regression data, trains a linear regression
    model, and saves the trained model to a file.

    Saves:
        A trained model to the file specified by `MODEL_PATH`.
    """
    # Generate synthetic data for regression
    X, y = make_regression(n_samples=1000, n_features=1, noise=10, random_state=42)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")


def predict_sales(features: list[float]) -> float:
    """
    Predict sales using the trained model.

    Args:
        features (list[float]): A list of feature values (e.g., marketing spend, etc.).

    Returns:
        float: Predicted sales value.

    Raises:
        FileNotFoundError: If the trained model file does not exist.
    """
    # Check if the model exists
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training a new model...")
        train_model()  # Automatically train the model if it doesn't exist
    
    # Load the trained model
    model = joblib.load(MODEL_PATH)
    
    # Convert features to a numpy array and reshape for prediction
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)
    return prediction[0]


def get_sales_prediction(features: list[float]) -> float:
    """
    Simulate a sales prediction based on input features.

    This is a simplified prediction logic that multiplies the sum of the features
    by a constant factor.

    Args:
        features (list[float]): A list of numerical feature values.

    Returns:
        float: Simulated sales prediction.
    """
    return sum(features) * 1.5  # Simple example of prediction logic


# Train the model when the script is executed
if __name__ == "__main__":
    train_model()