from rest_framework import permissions, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from api.tasks import send_reset_password_email_without_user
from users.models import Child, ChildrenGroup, User
from users.serializers import ChildSerializer, ChildrenGroupSerializer, EmailSerializer
from users.permissions import IsEducator, IsGroup, IsIndividual, IsParent


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет юзера.

    Доступно изменение метода сброса пароля reset_password
    на новом эндпоинте api/v1/reset_password/.
    """

    @action(
            methods=['post'],
            detail=False,
            permission_classes=(permissions.AllowAny,),
            serializer_class=EmailSerializer,
    )
    def reset_password(self, request, *args, **kwargs):
        """
        POST-запрос с адресом почты в json`е
        высылает ссылку на почту на подтвеждение смены пароля.
        Вид ссылки в письме:
        'https://our.site.name/password/reset/confirm/{uid}/{token}'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            User.objects.get(email__iexact=data.get('email'))
            send_reset_password_email_without_user.delay(data=data)
            return Response(status=status.HTTP_200_OK)
        except (User.DoesNotExist, AttributeError):
            return Response(
                {'detail': (
                    'Нет пользователя с введенным email или опечатка в адресе.'
                )},
                status=status.HTTP_204_NO_CONTENT
            )
        except User.MultipleObjectsReturned:
            return Response(
                {'detail': (
                    'В БД несколько юзеров с одним адресом почты.'
                    ' Отредактируйте дубликаты и повторите попытку.'
                )},
                status=status.HTTP_409_CONFLICT
            )


class ChildrenViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с карточкой ребенка.

    Доступ у пользователей с индивидуальным типом аккаунта
    (родители и логопеды).
    """
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (permissions.IsAuthenticated, IsParent)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsIndividual()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ChildrenGroupViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с группой.

    Доступ у пользователей с групповым типом аккаунта
    (педагоги).
    """
    queryset = ChildrenGroup.objects.all()
    serializer_class = ChildrenGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsEducator)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsGroup()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
