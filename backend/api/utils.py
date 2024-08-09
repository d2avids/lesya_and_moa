from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class Limit100OffsetPagination(LimitOffsetPagination):
    max_limit = 100
