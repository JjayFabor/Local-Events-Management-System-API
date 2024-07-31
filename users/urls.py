from django.urls import path, include
from .views import *
from .admin_views import *


urlpatterns = [
    path("admin/initial-create/", InitialAdminCreateView.as_view()),
    path("admin/create/", CreateAdminView.as_view()),
    path("users/register/", UserRegisterView.as_view()),
    path("users/login/", UserLoginView.as_view()),
    path("users/logout/", UserLogoutView.as_view()),
]
