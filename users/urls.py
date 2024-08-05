from django.urls import path
from .views import *
from .admin_views import *


urlpatterns = [
    path("admin/create/", CreateAdminView.as_view(), name="admin-create"),
    path("admin/login/", AdminUserLoginView.as_view(), name="admin-login"),
    path("admin/logout/", AdminUserLogoutView.as_view(), name="admin-logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "confirm-email/<int:user_id>/", ConfirmEmailView.as_view(), name="confirm-email"
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
