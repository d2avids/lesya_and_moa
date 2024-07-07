from rest_framework import permissions

from api.mixins import RetrieveListViewSet
from api.serializers import TaskSerializer
from tasks.models import Task


class TaskViewSet(RetrieveListViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny,)


