from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework import filters
from rest_framework import permissions

from api.mixins import RetrieveListViewSet
from api.serializers import TaskSerializer, RegionSerializer
from tasks.models import Task
from users.models import Region


class TaskViewSet(RetrieveListViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny,)


class RegionViewSet(RetrieveListViewSet):
    """Представляет регионы. Доступны только операции чтения."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (permissions.AllowAny,)
    ordering = ('name',)

    @method_decorator(cache_page(settings.REGIONS_LIST_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
