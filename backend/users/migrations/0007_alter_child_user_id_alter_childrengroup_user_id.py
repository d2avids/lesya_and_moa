# Generated by Django 5.0.6 on 2024-06-02 18:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_user_managers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Родитель/Логопед",
            ),
        ),
        migrations.AlterField(
            model_name="childrengroup",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children_groups",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Педагог",
            ),
        ),
    ]
