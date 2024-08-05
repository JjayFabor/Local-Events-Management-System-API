from django.urls import path, include
from .views import *


urlpatterns = [
    path("", EventView.as_view(), name="add-event"),
    path("categories/", CategoryListView.as_view(), name="list-categories"),
    path("categories/create/", CategoryCreateView.as_view(), name="create-categories"),
    path("categories/<int:pk>/", CategoryDeleteView.as_view(), name="delete-category"),
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
