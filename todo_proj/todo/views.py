from rest_framework import viewsets
from rest_framework import permissions

from .serializers import TaskSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Project, Task
from .filters import TaskFilter
from django_filters import rest_framework as filters


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = TaskFilter

    def get_queryset(self):
        return self.queryset.filter(project__owner=self.request.user)

