from rest_framework import serializers
from django.contrib.auth.models import User
from todo.models import Project, Task


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
