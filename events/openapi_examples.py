from drf_spectacular.utils import OpenApiExample

list_categories_example = OpenApiExample(
    "List of Categories",
    value=[{"id": 1, "name": "Education"}, {"id": 2, "name": "Sports"}],
    request_only=False,
    response_only=True,
)

create_category_request_example = OpenApiExample(
    "Create Category Request",
    value={"name": "Health"},
    request_only=True,
    response_only=False,
)

delete_category_success_example = OpenApiExample(
    "Delete Category Success",
    value={"message": "Category deleted successfully."},
    request_only=False,
    response_only=True,
)

delete_category_error_example = OpenApiExample(
    "Delete Category Error",
    value={"error": "Category not found"},
    request_only=False,
    response_only=True,
)

forbidden_example = OpenApiExample(
    "Forbidden",
    value={"detail": "You do not have permission to perform this action."},
    request_only=False,
    response_only=True,
)
