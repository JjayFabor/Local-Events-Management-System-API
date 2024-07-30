from django.urls import path, include
from .views import *


urlpatterns = [
    path("users/register/", UserRegisterView.as_view()),
]
