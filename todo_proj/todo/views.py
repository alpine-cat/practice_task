from rest_framework import viewsets
from rest_framework import permissions

from rest_framework_simplejwt import views as jwt_views
from rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.models import TokenUser

from .serializers import TaskSerializer, ProjectSerializer, UserSerializer, MyTokenSerializer
from django.contrib.auth.models import User
from .models import Project, Task
from .filters import TaskFilter
from django_filters import rest_framework as filters


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_class = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        return queryset.filter(username=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend,]
    filter_class = TaskFilter


class CustomAccessTokenView(jwt_views.TokenObtainPairView):
    serializer_class = MyTokenSerializer


class MyRegisterView(RegisterView):
    token_model = TokenUser

    def get_response_data(self, user):
        refresh = MyTokenSerializer.get_token(user)
        data = dict()

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {"pk": refresh.user.pk,
                        "username": str(refresh.user.username),
                        "email": str(refresh.user.email),
                        "first_name": str(refresh.user.first_name),
                        "last_name": str(refresh.user.last_name)
                        }

        return data

