# Generated by Django 5.0.6 on 2024-06-02 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='data_processing_agreement',
            field=models.BooleanField(default=True, verbose_name='согласие на обработку личных данных и подтверждение ознакомления с политикой конфиденциальности'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='example@ya.ru', max_length=254, verbose_name='Email'),
        ),
    ]
