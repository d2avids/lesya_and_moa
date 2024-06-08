from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views
from api.constants import POST_RESET_PASSWORD
from tasks import views as task_views
from users.views import CustomUserViewSet
from users import views as user_views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')
router.register(r'children', user_views.ChildrenViewSet, basename='children')
router.register(r'groups', user_views.ChildrenGroupViewSet, basename='groups')
router.register(r'answers/(?P<child_or_group_id>\d+)',
                task_views.TaskAnswerViewSet, basename='answers')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'reset_password/',
        CustomUserViewSet.as_view(POST_RESET_PASSWORD),
        name='reset_password'
    ),
]
