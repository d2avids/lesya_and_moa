from rest_framework import permissions

from users.models import Child, ChildrenGroup, User


class IsParentOrEducator(permissions.BasePermission):
    """
    Проверяет является ли пользователь родителем или учителем
    ребенка или группы, id которой передан в параметре пути.
    """

    def has_permission(self, request, view):
        user_type = request.user.tasks_type
        if user_type == User.INDIVIDUAL:
            child = Child.objects.filter(
                pk=request.resolver_match.kwargs.get('child_or_group_id')).first()
            if child and child.user == request.user:
                return True
        elif user_type == User.GROUP:
            children_group = ChildrenGroup.objects.filter(
                pk=request.resolver_match.kwargs.get('child_or_group_id')).first()
            if children_group and children_group.user == request.user:
                return True
        return False
