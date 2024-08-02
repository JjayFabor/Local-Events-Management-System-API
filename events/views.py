from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    tags=["Categories"],
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        201: CategorySerializer,
        400: ErrorSerializer,
        403: ErrorSerializer,
    },
    summary="Create and List Categories",
    description="This endpoint is Only for Admin user for creation of a new category or retrieving a list of all categories.",
    examples=[
        OpenApiExample(
            "List of Categories",
            value=[{"id": 1, "name": "Education"}, {"id": 2, "name": "Sports"}],
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            "Create Category Request",
            value={"name": "Health"},
            request_only=True,
            response_only=False,
        ),
    ],
)
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    tags=["Events"],
    request=EventSerializer,
    responses={
        201: EventSerializer,
        400: ErrorSerializer,
        403: ErrorSerializer,
    },
    summary="Create a new event",
    description="This endpoint allows an admin user only to create a new event.",
    examples=[
        OpenApiExample(
            "Create Event Example",
            value={
                "event_name": "Annual Tech Conference",
                "event_hosts": "Tech Innovators Inc.",
                "description": "A conference for technology enthusiasts to explore new trends.",
                "image_url": "https://example.com/images/tech-conference.jpg",
                "event_date": "2024-09-15T09:00:00Z",
                "category": 1,
                "location": "Tech Convention Center, Silicon Valley",
                "registration_deadline": "2024-09-01T23:59:59Z",
                "capacity": 500,
                "status": "UPCOMING",
            },
            request_only=True,
            response_only=False,
        ),
    ],
)
class EventView(generics.CreateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["Events"],
    request=None,
    responses={
        200: EventSerializer(many=True),
        400: ErrorSerializer,
    },
    summary="List Available Events",
    description="This endpoint allows any authenticated user to retrieve a list of available events.",
    examples=[
        OpenApiExample(
            "List of Events",
            value=[
                {
                    "id": 1,
                    "event_name": "Annual Tech Conference",
                    "event_hosts": "Tech Innovators Inc.",
                    "description": "A conference for technology enthusiasts to explore new trends.",
                    "image_url": "https://example.com/images/tech-conference.jpg",
                    "event_date": "2024-09-15T09:00:00Z",
                    "category": 1,
                    "location": "Tech Convention Center, Silicon Valley",
                    "registration_deadline": "2024-09-01T23:59:59Z",
                    "capacity": 500,
                    "status": "UPCOMING",
                }
            ],
            request_only=False,
            response_only=True,
        ),
    ],
)
class ListEventView(generics.ListAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
