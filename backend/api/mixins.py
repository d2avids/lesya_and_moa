from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class RetrieveListViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    pass
