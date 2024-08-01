from django.urls import path, include
from .views import *
from .admin_views import *


urlpatterns = [
    path("admin/initial-create/", InitialAdminCreateView.as_view()),
    path("admin/create/", CreateAdminView.as_view()),
    path("admin/login/", AdminUserLoginView.as_view()),
    path("admin/logout/", AdminUserLogoutView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
]
