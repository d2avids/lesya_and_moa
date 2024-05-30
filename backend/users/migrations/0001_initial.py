# Generated by Django 5.0.6 on 2024-05-30 05:30

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('tasks_type', models.CharField(choices=[('индивидуальный', 'индивидуальный'), ('групповой', 'групповой')], default='индивидуальный', max_length=20, verbose_name='Формат занятий')),
                ('data_processing_agreement', models.BooleanField(verbose_name='согласие на обработку личных данных и подтверждение ознакомления с политической конфиденциальностью')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ChildrenGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Данное поле должно содержать только кириллицу, числа, "-", "", и «»', regex='^[а-яА-ЯёЁ0-9"«» -]+$')], verbose_name='Название группы')),
                ('number_of_students', models.PositiveIntegerField(error_messages={'invalid': 'Количество учеников должно быть от 1 до 50'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)], verbose_name='Количество учеников в группе')),
                ('average_age', models.DecimalField(decimal_places=2, error_messages={'invalid': 'Средний возраст должен быть от 1 до 99'}, max_digits=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Средний возраст учеников группы')),
                ('school', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Данное поле должно содержать только кириллицу, числа, "-", №, "", и «»', regex='^[а-яА-ЯёЁ0-9№"«» -]+$')], verbose_name='Школа')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children_groups', to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт привязки')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Группа детей',
                'verbose_name_plural': 'Группы детей',
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Данное поле должно содержать только буквы кириллицы и знак "-"', regex='^[а-яА-ЯёЁ-]+$')], verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Данное поле должно содержать только буквы кириллицы и знак "-"', regex='^[а-яА-ЯёЁ-]+$')], verbose_name='Фамилия')),
                ('sex', models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], default='Мужской', max_length=10, verbose_name='Пол')),
                ('age', models.PositiveIntegerField(error_messages={'invalid': 'Поле заполнено не верно'}, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Возраст')),
                ('school', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Данное поле должно содержать только кириллицу, числа, "-", №, "", и «»', regex='^[а-яА-ЯёЁ0-9№"«» -]+$')], verbose_name='Школа')),
                ('grade', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Класс')),
                ('attended_speech_therapist', models.BooleanField(default=False, verbose_name='Посещал ли ребенок раньше логопеда?')),
                ('data_processing_agreement', models.BooleanField(verbose_name='согласие на обработку личных данных и подтверждение ознакомления с политической конфиденциальностью')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт привязки')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Ребенок',
                'verbose_name_plural': 'Дети',
            },
        ),
    ]
