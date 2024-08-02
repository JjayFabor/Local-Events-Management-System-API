from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import *
from .serializers import *
from users.serializers import CustomUserSerializer
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)


@extend_schema_view(
    get=extend_schema(
        tags=["Categories"],
        summary="List Categories",
        description="Retrieve a list of all categories. Only accessible by Admin users.",
        responses={
            200: CategorySerializer(many=True),
            403: OpenApiResponse(
                response=ErrorSerializer,
                description="User does not have permission",
                examples=[
                    OpenApiExample(
                        "Forbidden",
                        value={
                            "detail": "You do not have permission to perform this action."
                        },
                        request_only=False,
                        response_only=True,
                    )
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "List of Categories",
                value=[{"id": 1, "name": "Education"}, {"id": 2, "name": "Sports"}],
                request_only=False,
                response_only=True,
            ),
        ],
    ),
    post=extend_schema(
        tags=["Categories"],
        summary="Create Category",
        description="Create a new category. Only accessible by Admin users.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: ErrorSerializer,
            403: OpenApiResponse(
                response=ErrorSerializer,
                description="User does not have permission",
                examples=[
                    OpenApiExample(
                        "Forbidden",
                        value={
                            "detail": "You do not have permission to perform this action."
                        },
                        request_only=False,
                        response_only=True,
                    )
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "Create Category Request",
                value={"name": "Health"},
                request_only=True,
                response_only=False,
            ),
        ],
    ),
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
                "category_name": "Education",
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
                    "category": "Education",
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


@extend_schema(
    tags=["Events"],
    request=None,
    responses={
        200: {
            "description": "Event registration successful.",
            "content": {
                "application/json": {
                    "example": {"message": "Event registration successful."},
                }
            },
        },
        400: {
            "description": "Event ID Missing or Bad Request",
            "content": {
                "application/json": {
                    "example": {"error": "Event ID is required"},
                }
            },
        },
        404: {
            "description": "Event Not Found",
            "content": {
                "application/json": {
                    "example": {"error": "Event not found"},
                }
            },
        },
        403: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Authentication credentials were not provided."
                    },
                }
            },
        },
    },
    parameters=[
        OpenApiParameter(
            name="event_id",
            type=int,
            description="ID of the event to register for",
            required=True,
            location=OpenApiParameter.PATH,
        )
    ],
    summary="Register for an Event",
    description="This endpoint allows an authenticated user to register for an event by providing the event ID in the URL path.",
)
class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, *args, **kwargs):
        user = request.user
        try:
            event = EventModel.objects.get(id=event_id)
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.events_joined.add(event)
        event.participants.add(user)
        return Response(
            {"message": "Event registration successful."}, status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Events"],
    parameters=[
        OpenApiParameter(
            "event_id",
            description="ID of the event to retrieve details for",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: EventDetailSerializer,
        404: ErrorSerializer,
    },
    description="Retrieve the details of an event and its participants.",
)
class EventDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, *args, **kwargs):
        try:
            event = EventModel.objects.get(id=event_id)
            event_data = EventSerializer(event).data
            participants_data = CustomUserSerializer(
                event.participants.all(), many=True
            ).data
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"event": event_data, "participants": participants_data},
            status=status.HTTP_200_OK,
        )
