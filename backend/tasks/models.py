from django.core.exceptions import ValidationError
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'{self.pk} - {self.name}'


class TaskAnswer(models.Model):
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Задание'
    )
    children_group = models.ForeignKey(
        'users.ChildrenGroup',
        on_delete=models.CASCADE,
        related_name='tasks_answers',
        blank=True,
        null=True,
        verbose_name='Группа детей'
    )
    child = models.ForeignKey(
        'users.Child',
        on_delete=models.CASCADE,
        related_name='tasks_answers',
        blank=True,
        null=True,
        verbose_name='Ребенок'
    )
    is_correct = models.BooleanField(verbose_name='Верность ответа')
    is_started = models.BooleanField(verbose_name='Факт прохождения задания')

    class Meta:
        verbose_name_plural = 'Ответы на задания'
        verbose_name = 'Ответ на задание'

    def clean(self):
        if not self.children_group and not self.children:
            raise ValidationError('Заполните одно из полей: "Группа детей" или "Ребенок".')
        if self.children_group and self.children:
            raise ValidationError('Одновременно можно заполнить только одно поле: "Группа детей" или "Ребенок".')

    def __str__(self):
        return f'Ответ на задание {self.task.pk}, {"Группа детей" if self.children_group else "Ребенок"}'

    def save(self, *args, **kwargs):
        self.clean()
        super(TaskAnswer, self).save(*args, **kwargs)
