from rest_framework import routers
from .views import ProjectViewSet, UserViewSet, TaskViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)

