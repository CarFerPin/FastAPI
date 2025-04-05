# FastAPI Application

This project is a FastAPI-based application that provides a robust backend for managing items, users, and sales predictions. It includes features such as authentication, CRUD operations, and machine learning-based sales predictions.

## Features

1. **User Management**:
   - Create new users.
   - Retrieve user details by username.
   - Secure user authentication with hashed passwords and JWT tokens.

2. **Item Management**:
   - Create, retrieve, update, and delete items.
   - Manage item availability status.

3. **Sales Prediction**:
   - Predict sales based on input features using a trained machine learning model.

4. **Authentication**:
   - Secure endpoints with OAuth2 and JWT-based authentication.
   - Token-based access control for users.

5. **Middlewares**:
   - Logging middleware for tracking requests and responses.
   - CORS middleware for cross-origin resource sharing.

6. **Database**:
   - SQLAlchemy-based database models and session management.
   - SQLite database for local development.

7. **Logging**:
   - Centralized logging for database changes and application events.

## Endpoints

### Authentication
- **POST** `/token`: Obtain an access token by providing username and password.

### User Management
- **POST** `/users/`: Create a new user.
- **GET** `/users/{username}`: Retrieve user details by username.

### Item Management
- **POST** `/items/`: Create a new item.
- **GET** `/items/`: Retrieve all items.
- **GET** `/items/{item_id}`: Retrieve an item by ID.
- **PUT** `/items/{item_id}`: Update an item by ID.
- **PATCH** `/items/{item_id}`: Partially update an item by ID.
- **DELETE** `/items/{item_id}`: Delete an item by ID.

### Sales Prediction
- **POST** `/predict-sales/`: Predict sales based on input features.

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
uvicorn app.main:app --reload

## Usage (Example)

1. Access the API documentation:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc



2. Example Usage (curl)
Create a User:
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
}'

3. Predict Sales:
curl -X POST "http://127.0.0.1:8000/predict-sales/" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{
    "features": [50.0]
}'

## License and Contributiong

1. License
This project is licensed under the MIT License. See the LICENSE file for details.

2. Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.