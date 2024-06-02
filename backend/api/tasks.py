import logging

from celery import shared_task
from rest_framework import status
from rest_framework.response import Response

from api.email import CustomPasswordResetEmail
from users.models import User

logger = logging.getLogger('tasks')


@shared_task
def send_reset_password_email_without_user(data: dict):
    """Отправка письма о смене пароля без токена."""

    email = data.get('email').lower()
    email_list = [email,]
    try:
        user = User.objects.get(email=email)
        CustomPasswordResetEmail(email=email, user=user).send(email_list)
        logger.info(
            'Письмо смены пароля отправлено.'
        )
    except (User.DoesNotExist, AttributeError):
        return Response(
            {'detail': 'Ошибка в email-адресе'},
            status=status.HTTP_204_NO_CONTENT
        )