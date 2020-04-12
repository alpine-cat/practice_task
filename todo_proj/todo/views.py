from rest_framework import viewsets
from rest_framework import permissions

from .serializers import TaskSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Project, Task
from .filters import TaskFilter, ProjectFilter
from django_filters import rest_framework as filters


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_class = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    filter_class = ProjectFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = TaskFilter


