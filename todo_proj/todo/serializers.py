from rest_framework import serializers
from django.contrib.auth.models import User
from todo.models import Project, Task
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'project', 'task', 'date', 'status', 'priority')
        ordering = ['priority']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'url', 'color', 'project_name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = ProjectSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'projects')


class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.user = User.objects.get(username=user.username)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {"pk": refresh.user.pk,
        "username": str(refresh.user.username),
        "email": str(refresh.user.email),
        "first_name": str(refresh.user.first_name),
        "last_name": str(refresh.user.last_name)
                         }

        return data


