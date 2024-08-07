from rest_framework.permissions import BasePermission

from users.models import User


class IsParent(BasePermission):
    """
    Пермишен для доступа к данным ребенка.

    Доступ только логопеду и родителю.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tasks_type == User.INDIVIDUAL)

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class IsGroup(BasePermission):
    """
    Пермишен для доступа к данным группы.

    Доступ только педагогу.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tasks_type == User.GROUP)

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id


class IsIndividual(BasePermission):
    """
    Пермишен для доступа добавления ребенка.

    Доступ только логопеду и родителю.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tasks_type == User.INDIVIDUAL)


class IsEducator(BasePermission):
    """
    Пермишен для доступа к данным группы.

    Доступ только педагогу.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tasks_type == User.GROUP)

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
