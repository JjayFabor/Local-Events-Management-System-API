import django_filters
from .models import EventModel


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    date = django_filters.DateFilter()
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )

    class Meta:
        model = EventModel
        fields = ["name", "location", "date", "category"]
