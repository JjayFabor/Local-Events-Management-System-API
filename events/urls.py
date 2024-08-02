from django.urls import path, include
from .views import *


urlpatterns = [
    path("", EventView.as_view()),
    path("category/", CategoryView.as_view()),
    path("event-list/", ListEventView.as_view()),
]
