from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework import filters
from rest_framework import permissions

from api.mixins import RetrieveListViewSet
from api.serializers import TaskSerializer, RegionSerializer, ShortNewsSerializer, NewsSerializer
from api.utils import Limit100OffsetPagination
from news.models import News
from tasks.models import Task
from users.models import Region


class TaskViewSet(RetrieveListViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(settings.TASKS_LIST_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class NewsViewSet(RetrieveListViewSet):
    queryset = News.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = Limit100OffsetPagination

    @method_decorator(cache_page(settings.TASKS_LIST_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return ShortNewsSerializer
            case 'retrieve':
                return NewsSerializer
            case _:
                return NewsSerializer


class RegionViewSet(RetrieveListViewSet):
    """Представляет регионы. Доступны только операции чтения."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (permissions.IsAuthenticated,)
    ordering = ('name',)

    @method_decorator(cache_page(settings.REGIONS_LIST_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
