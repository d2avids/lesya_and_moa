# Generated by Django 5.0.6 on 2024-08-09 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_name_alter_taskanswer_is_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskanswer',
            name='is_started',
            field=models.BooleanField(default=True, verbose_name='Задание начато'),
        ),
    ]
