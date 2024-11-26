I'll convert the document to GitHub-flavored Markdown with appropriate formatting and JSON code blocks.

# Project Title

This project is a Django-based backend application that provides authentication and user management functionalities. It includes features such as user registration, login, logout, password management, and token-based authentication.

## Project Structure

```
.env
.gitignore
.idea/
authentication/
    __init__.py
    admin.py
    apps.py
    decorators.py
    migrations/
    model/
        base.py
        users.py
    models.py
    serializer/
        users.py
    serializers.py
    tests.py
    urls.py
    utils.py
    views.py
backend/
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
db.sqlite3
manage.py
media/
Pipfile
Pipfile.lock
requirements.txt
reset_db.bat
```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/bene-volent/django-auth-backend.git
    cd django-auth-backend
    ```

2. Create and activate a virtual environment using Pipenv:
    ```bash
    python -m pip install pipenv
    pipenv install
    pipenv shell
    ```
3. Generate secret keys for project (SECRET_KEY, JWT_SECRET):
  ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
4. Create a `.env` file in the root directory and add the following environment variables:
    ```
    SECRET_KEY='your-secret-key'
    DEBUG=True
    JWT_SECRET='your-jwt-secret'
    JWT_ALGORITHM=HS256
    JWT_EXPIRATION_DELTA=864000
    DATABASE_URL=sqlite:///db.sqlite3
    STORE_TOKEN_IN_HTTP_ONLY_COOKIE=False
    ```

5. Apply the migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoints

#### User Endpoints

##### User Registration: `POST /api/auth/users/`
- Registers a new user.
- Request body:
    ```json
    {
        "fname": "John",
        "lname": "Doe",
        "email": "john.doe@example.com",
        "password": "Password123!",
        "bio": "A short bio",
        "role": "user",
        "is_verified": true
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A short bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### User Login: `POST /api/auth/login`
- Logs in a user and returns a JWT token.
- Request body:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "Password123!"
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A short bio",
            "role": "user",
            "is_verified": true
        },
        "token": "jwt-token"
    }
    ```

##### User Logout: `POST /api/auth/logout`
- Logs out a user.
- Response:
    ```json
    {
        "message": "Logged out successfully"
    }
    ```

##### Change Password: `POST /api/auth/change-password`
- Changes the password of a user.
- Request body:
    ```json
    {
        "email": "john.doe@example.com",
        "current-password": "Password123!",
        "new-password": "NewPassword123!"
    }
    ```
- Response:
    ```json
    {
        "message": "Password changed successfully"
    }
    ```

##### Login Status: `GET /api/auth/login-status`
- Checks the login status of a user.
- Response:
    ```json
    {
        "status": true
    }
    ```

##### User Details: `GET /api/auth/users/me`
- Retrieves the details of the authenticated user.
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A short bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Update User Details: `PUT /api/auth/users/me`
- Updates the details of the authenticated user.
- Request body:
    ```json
    {
        "fname": "John",
        "lname": "Doe",
        "bio": "An updated bio"
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "An updated bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Partial Update User Details: `PATCH /api/auth/users/me`
- Partially updates the details of the authenticated user.
- Request body:
    ```json
    {
        "bio": "A partially updated bio"
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A partially updated bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Delete User: `DELETE /api/auth/users/me`
- Deletes the authenticated user.
- Response:
    ```json
    {
        "message": "User deleted successfully"
    }
    ```

#### Admin Endpoints

##### List Users: `GET /api/auth/users/`
- Lists all users (admin only).
- Response:
    ```json
    {
        "users": [
            {
                "fname": "John",
                "lname": "Doe",
                "email": "john.doe@example.com",
                "bio": "A short bio",
                "role": "user",
                "is_verified": true
            },
            ...
        ]
    }
    ```

##### Retrieve User: `GET /api/auth/users/{id}`
- Retrieves the details of a specific user (admin only).
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A short bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Update User: `PUT /api/auth/users/{id}`
- Updates the details of a specific user (admin only).
- Request body:
    ```json
    {
        "fname": "John",
        "lname": "Doe",
        "bio": "An updated bio"
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "An updated bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Partial Update User: `PATCH /api/auth/users/{id}`
- Partially updates the details of a specific user (admin only).
- Request body:
    ```json
    {
        "bio": "A partially updated bio"
    }
    ```
- Response:
    ```json
    {
        "user": {
            "fname": "John",
            "lname": "Doe",
            "email": "john.doe@example.com",
            "bio": "A partially updated bio",
            "role": "user",
            "is_verified": true
        }
    }
    ```

##### Delete User: `DELETE /api/auth/users/{id}`
- Deletes a specific user (admin only).
- Response:
    ```json
    {
        "message": "User deleted successfully"
    }
    ```

## Future Improvements

- Enhanced Security: Implement additional security measures such as rate limiting, IP whitelisting, and two-factor authentication.
- User Activity Logging: Add logging for user activities to monitor and audit user actions.
- Email Verification: Implement email verification for new user registrations.
- Password Reset: Add functionality for users to reset their passwords via email.
- API Documentation: Improve API documentation using tools like Swagger or Redoc.
- Role-Based Access Control: Implement more granular role-based access control (RBAC) to manage permissions more effectively.
- Scalability: Optimize the application for scalability, including database optimization and load balancing.
- Automated Testing: Add comprehensive unit and integration tests to ensure the reliability and stability of the application.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

This README provides an overview of the project, including installation instructions, usage details, and future improvement suggestions. For more detailed information, refer to the individual files and their respective documentation.
