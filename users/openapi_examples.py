# my_app/openapi_examples.py
from drf_spectacular.utils import OpenApiExample

# Example for regular user registration
regular_user_example = OpenApiExample(
    "Regular User",
    summary="Example of a regular user registration",
    description="Example payload for registering a regular user",
    value={
        "email": "test_user@example.com",
        "password": "userpassword",
        "first_name": "Test",
        "last_name": "User",
    },
    request_only=True,
)

# Example for initial admin user registration
admin_user_example = OpenApiExample(
    "Admin User",
    summary="Example of an admin user registration",
    description="Example payload for registering an admin user",
    value={
        "email": "test_admin@example.com",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
    },
    request_only=True,
)


# Example for admin user registration
admin2_user_example = OpenApiExample(
    "Admin User",
    summary="Example of an admin user registration",
    description="Example payload for registering an admin user",
    value={
        "email": "test_admin2@example.com",
        "password": "admin2password",
        "first_name": "Admin2",
        "last_name": "User",
    },
    request_only=True,
)
