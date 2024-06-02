from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views
from api.constants import POST_RESET_PASSWORD
from users.views import CustomUserViewSet

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'reset_password/',
        CustomUserViewSet.as_view(POST_RESET_PASSWORD),
        name='reset_password'
    ),
]
