from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EventModel(models.Model):
    UPCOMING = "UPCOMING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    STATUS_CHOICES = {
        UPCOMING: "UPCOMING",
        ONGOING: "ONGOING",
        COMPLETED: "COMPLETED",
        CANCELED: "CANCELED",
    }

    event_name = models.CharField(max_length=100)
    event_hosts = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image_url = models.URLField(max_length=200)
    event_date = models.DateTimeField(blank=False, auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    registration_deadline = models.DateTimeField(blank=False, auto_now_add=False)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=UPCOMING)

    class Meta:
        permissions = [
            ("view_event", "Can view event"),
            ("change_event", "Can change event"),
            ("delete_event", "Can delete event"),
            ("add_event", "Can add event"),
        ]

    def __str__(self):
        return self.event_name
