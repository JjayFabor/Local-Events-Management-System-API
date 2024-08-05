from django.urls import path, include
from .views import *


urlpatterns = [
    path("", EventView.as_view(), name="add-event"),
    path("categories/", CategoryView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryView.as_view(), name="category-delete"),
    path("event-list/", ListEventView.as_view(), name="list-event"),
    path(
        "register-event/<int:event_id>/",
        EventRegistrationView.as_view(),
        name="register-event",
    ),
    path(
        "event-detail/<int:event_id>/", EventDetailView.as_view(), name="event-detail"
    ),
]
