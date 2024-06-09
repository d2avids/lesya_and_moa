from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    OpenApiParameter, extend_schema, extend_schema_view, inline_serializer
)

from .models import Task, TaskAnswer
from .serializers import TaskAnswerSerializer, TaskAnswerUpdateSerializer
from .permissions import IsParentOrEducator
from users.models import Child, ChildrenGroup, User


@extend_schema_view(
    list=extend_schema(
        description='Получить ответы на задания конкретного ребенка или группы детей.',
        summary='Получить ответы на задания конкретного ребенка или группы детей.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            )
        ]
    ),
    create=extend_schema(
        description=('Здесь создается экземпляр TaskAnswer и '
                     'задается флаг is_started=True.\n\n'
                     'При начале выполнения задания необходимо '
                     'отправить post запрос с id задания'),
        summary='Начать выполнение задания.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            )
        ],
        request=inline_serializer(
            name='InlineFormSerializer',
            fields={
                'task': serializers.IntegerField(),
            },
        ),
    ),
    update=extend_schema(
        description='Здесь меняется флаг is_correct.\n\n'
                    'Принимает флаг is_correct=True. '
                    'В параметре пути id это id ответа на задание '
                    '(экземпляра TaskAnswer).',
        summary='Отметить задание выполненным.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            ),
            OpenApiParameter(
                'id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ответа на задание',
            )
        ],
        request=inline_serializer(
            name='InlineSerializer',
            fields={
                'is_correct': serializers.BooleanField(),
            },
        ),
    ),
    partial_update=extend_schema(
        description='Здесь меняется флаг is_correct.\n\n'
                    'Принимает флаг is_correct=True. '
                    'В параметре пути id это id ответа на задание '
                    '(экземпляра TaskAnswer).',
        summary='Отметить задание выполненным.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            ),
            OpenApiParameter(
                'id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ответа на задание',
            )
        ],
        request=inline_serializer(
            name='InlineSerializer',
            fields={
                'is_correct': serializers.BooleanField(),
            },
        ),
    ),
    retrieve=extend_schema(
        description='Получить ответ на задание конкретного ребенка или группы детей.',
        summary='Получить ответ на задание конкретного ребенка или группы детей.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            ),
            OpenApiParameter(
                'id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ответа на задание',
            )
        ]
    ),
    destroy=extend_schema(
        description='Удалить ответ на задание.',
        summary='Удалить ответ на задание.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            ),
            OpenApiParameter(
                'id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ответа на задание',
            )
        ]
    ),
    check_progress=extend_schema(
        description='Проверить прогресс выполнения задания.',
        summary='Проверить прогресс выполнения задания.',
        parameters=[
            OpenApiParameter(
                'child_or_group_id',
                int,
                OpenApiParameter.PATH,
                required=True,
                description='id ребенка или группы детей',
            ),
        ],
        responses=inline_serializer(
            name='InlineSerializerProgress',
            fields={
                'progress': serializers.IntegerField()
            }
        )
    )
)
class TaskAnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с ответами на задания.

    В параметре пути передается id ребенка или группы детей.\n
    При старте задания необходимо отправить post запрос с
    id задания и флагом is_started=True.
    В ответ вернется экземпляр TaskAnswer.\n
    При успешном завершении задания нужно отправить PUT или
    PATCH запрос ('id' в параметре пути - id экземпляра TaskAnswer)
    c флагом is_correct=True.
    GET list запрос возвращает ответы на задание для конкретного
    ребенка или группы детей.
    """
    serializer_class = TaskAnswerSerializer
    permission_classes = (permissions.IsAuthenticated, IsParentOrEducator)

    def get_queryset(self):
        if self.request.user.tasks_type == User.GROUP:
            return TaskAnswer.objects.filter(
                children_group__user=self.request.user,
                children_group_id=self.kwargs.get('child_or_group_id')
            )
        return TaskAnswer.objects.filter(
            child__user=self.request.user,
            child_id=self.kwargs.get('child_or_group_id')
        )

    def perform_create(self, serializer):
        if self.request.user.tasks_type == User.GROUP:
            serializer.save(
                children_group_id=self.kwargs.get('child_or_group_id'))
        else:
            serializer.save(
                child_id=self.kwargs.get('child_or_group_id'))

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return TaskAnswerUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False,
            methods=['get'])
    def check_progress(self, request, child_or_group_id, *args, **kwargs):
        user_type = request.user.tasks_type
        count_questions = Task.objects.count()
        if user_type == User.INDIVIDUAL:
            count_tasks_answers = TaskAnswer.objects.filter(
                child_id=child_or_group_id
            ).count()
            return Response(
                {'progress': round(count_tasks_answers / count_questions * 100)}
            )
        elif user_type == User.GROUP:
            count_tasks_answers = TaskAnswer.objects.filter(
                children_group_id=child_or_group_id
            ).count()
            return Response(
                {'progress': round(count_tasks_answers / count_questions * 100)}
            )
