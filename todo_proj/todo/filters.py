import django_filters as filters
from .models import Task, STATUS
from datetime import date
from datetime import timedelta


class TaskFilter(filters.FilterSet):
    project = filters.CharFilter(field_name='project__id')
    date_ch = filters.DateFilter(field_name='date', lookup_expr='lte')
    status = filters.ChoiceFilter(field_name='status', choices=STATUS)
    owner = filters.CharFilter(field_name='project__owner__username')

    class Meta:
        filter_model = Task