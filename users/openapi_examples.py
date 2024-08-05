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

user_response_example = OpenApiExample(
    "User Response Example",
    summary="Example of a successful user registration response",
    description="This example shows the response after a successful user registration",
    value={
        "message": "Check your email for account confirmation",
        "user": {
            "id": 1,
            "email": "newuser@example.com",
            "username": "newuser",
            "is_active": False,
        },
    },
    response_only=True,
)

error_response_example = OpenApiExample(
    "Error Response Example",
    summary="Example of a failed registration response",
    description="This example shows the response after a failed registration due to validation errors",
    value={
        "email": ["This field is required."],
        "password": ["This field is required."],
    },
    response_only=True,
)

success_confirm_example = OpenApiExample(
    "Successful Email Confirmation Example",
    summary="Example of a successful email confirmation",
    description="This example shows the response after a successful email confirmation",
    value={"message": "Email confirmed, you can now log in."},
    response_only=True,
)

error_confirm_example = OpenApiExample(
    "Error Email Confirmation Example",
    summary="Example of a failed email confirmation",
    description="This example shows the response when the confirmation link is invalid",
    value={"message": "Invalid Confirmation Link."},
    response_only=True,
)


login_successful_example = OpenApiExample(
    "Successful Login",
    summary="A successful login example",
    description="Example of a successful login response",
    value={"message": "Login successful", "csrf_token": "csrf-token-value"},
    response_only=True,
    status_codes=["200"],
)

login_invalid_credentials_example = OpenApiExample(
    "Invalid Credentials",
    summary="An unsuccessful login example",
    description="Example of an unsuccessful login response due to invalid credentials",
    value={"error": "Invalid Credentials"},
    response_only=True,
    status_codes=["400"],
)

authenticated_user_example = OpenApiExample(
    "Authenticated User",
    summary="Example of a successful response with authenticated user data",
    description="Returns the details of the authenticated user",
    value={
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "events_joined": ["list of events the user has joined"],
    },
    response_only=True,
    status_codes=["200"],
)

unauthenticated_user_example = OpenApiExample(
    "Unauthenticated User",
    summary="Example of an unauthenticated response",
    description="Returns an error message when the user is not authenticated",
    value={"error": "User is not authenticated"},
    response_only=True,
    status_codes=["400"],
)


retrieve_user_profile_examples = [
    OpenApiExample(
        "Successful Response",
        value={
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
        },
        response_only=True,
        status_codes=["200"],
    ),
]

update_user_profile_examples = [
    OpenApiExample(
        "Update Request",
        value={"first_name": "John", "last_name": "Doe"},
        request_only=True,
    ),
    OpenApiExample(
        "Successful Response",
        value={
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
        },
        response_only=True,
        status_codes=["200"],
    ),
]
