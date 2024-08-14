from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class Limit100OffsetPagination(LimitOffsetPagination):
    max_limit = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.total_count = queryset.count()

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'total': self.total_count,
            'count': len(data),
            'limit': self.limit,
            'offset': self.offset,
            'results': data
        })