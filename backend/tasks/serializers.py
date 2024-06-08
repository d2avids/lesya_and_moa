from rest_framework import serializers

from .models import Task, TaskAnswer
from users.models import Child, ChildrenGroup, User
from users.serializers import (
    ShortChildSerializer, ShortChildrenGroupSerializer
)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskAnswerSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),
                                              write_only=True)
    children_group = ShortChildrenGroupSerializer(read_only=True)
    child = ShortChildSerializer(read_only=True)

    class Meta:
        model = TaskAnswer
        fields = (
            'id',
            'task',
            'children_group',
            'child',
            'is_correct',
            'is_started'
        )
        read_only_fields = (
            'id',
            'children_group',
            'child',
            'is_started',
            'task'
        )

    def validate(self, data):
        request = self.context.get('request')
        user_type = request.user.tasks_type
        if request.method == 'POST':
            if user_type == User.INDIVIDUAL:
                child = Child.objects.get(
                    pk=request.resolver_match.kwargs.get('child_or_group_id'))
                children_group = None
            else:
                children_group = ChildrenGroup.objects.get(
                    pk=request.resolver_match.kwargs.get('child_or_group_id'))
                child = None
            if TaskAnswer.objects.filter(
                    task=data.get('task'),
                    children_group=children_group,
                    child=child,
            ).exists():
                raise serializers.ValidationError('Такой ответ уже есть')
            if request.data.get('is_started') and request.data.get('is_correct'):
                raise serializers.ValidationError(
                    'Для завершения задания (изменения is_correct) нужно '
                    'отправить PUT или PATCH запрос')
        return data

    def to_representation(self, instance):
        self.fields['task'] = TaskSerializer(read_only=True)
        return super().to_representation(instance)


class TaskAnswerUpdateSerializer(serializers.ModelSerializer):
    task = TaskAnswerSerializer(read_only=True)
    children_group = ShortChildrenGroupSerializer(read_only=True)
    child = ShortChildSerializer(read_only=True)

    class Meta:
        model = TaskAnswer
        fields = (
            'id',
            'task',
            'children_group',
            'child',
            'is_correct',
            'is_started'
        )
        read_only_fields = ('id', 'children_group', 'child', 'is_started', 'task')

    def validate(self, attrs):
        request = self.context.get('request')
        task_answer = TaskAnswer.objects.filter(
            id=request.resolver_match.kwargs.get('pk')).first()
        if task_answer and task_answer.is_correct:
            raise serializers.ValidationError(
                f'Задание {task_answer.task} уже пройдено')
        elif not task_answer:
            raise serializers.ValidationError('Такого ответа нет')
        return super().validate(attrs)
