from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, EventModel
from .serializers import (
    CategorySerializer,
    EventSerializer,
    ErrorSerializer,
    EventDetailSerializer,
    EventRegistrationResponseSerializer,
)
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
        200: EventRegistrationResponseSerializer,
        400: EventRegistrationResponseSerializer,
        404: EventRegistrationResponseSerializer,
        403: EventRegistrationResponseSerializer,
        405: EventRegistrationResponseSerializer,
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
    description="This endpoint allows an authenticated user to register for an event by providing the event ID in the URL path. It ensures that the user can only register once and checks if the event has reached its capacity.",
)
class EventRegistrationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventRegistrationResponseSerializer

    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(EventModel, id=event_id)
        user = request.user

        # check if the user already registered
        if event.participants.filter(id=user.id).exists():
            return Response(
                {"message": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the participants exceed the capacity
        total_participants = event.participants.count()
        if total_participants >= event.capacity:
            return Response(
                {"message": "Event is full"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        user.events_joined.add(event)
        event.participants.add(user)

        # Recalculate the total participants after adding the user
        total_participants = event.participants.count()
        return Response(
            {
                "message": "Event registration successful.",
                "total_participants": total_participants,
            },
            status=status.HTTP_200_OK,
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
    queryset = EventModel.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(EventModel, id=self.kwargs["event_id"])
