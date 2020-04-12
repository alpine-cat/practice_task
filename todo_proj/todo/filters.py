import django_filters as filters
from .models import Task, TASK_STATUS, Project


class TaskFilter(filters.FilterSet):
    project = filters.CharFilter(field_name='project__id')
    date_ch = filters.DateFilter(field_name='date', lookup_expr='lte')
    status = filters.ChoiceFilter(field_name='status', choices=TASK_STATUS)
    owner = filters.CharFilter(field_name='project__owner__username')

    class Meta:
        filter_model = Task


class ProjectFilter( filters.FilterSet):
    owner = filters.CharFilter(field_name='owner__username')

    class Meta:
        filter_model = Project
