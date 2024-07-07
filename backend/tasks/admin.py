from django.contrib import admin

from tasks.models import Task, TaskAnswer


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(TaskAnswer)
class TaskAnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'task', 'children_group', 'child', 'is_correct', 'is_started')
