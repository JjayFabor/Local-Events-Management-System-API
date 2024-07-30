from django.urls import path, include
from .views import *


urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
    path("users/login/", UserLoginView.as_view()),
    path("users/logout/", UserLogoutView.as_view()),
]
