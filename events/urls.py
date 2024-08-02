from django.urls import path, include
from .views import *


urlpatterns = [
    path("", EventView.as_view(), name="add-event"),
    path("category/", CategoryView.as_view(), name="add-category"),
    path("event-list/", ListEventView.as_view(), name="list-event"),
    path(
        "register-event/<int:event_id>/",
        EventRegistrationView.as_view(),
        name="register-event",
    ),
]
