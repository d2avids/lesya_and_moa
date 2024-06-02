from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    RegexValidator)
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tasks_type',]
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        default='example@ya.ru',
        unique=True,
        blank=False,
        null=False
    )
    username = None
    INDIVIDUAL = 'индивидуальный'
    GROUP = 'групповой'

    EXERCISE_CHOICES = [
        (INDIVIDUAL, 'индивидуальный'),
        (GROUP, 'групповой'),
    ]

    tasks_type = models.CharField(
        verbose_name='Формат занятий',
        max_length=20,
        choices=EXERCISE_CHOICES,
        default=INDIVIDUAL,
    )
    data_processing_agreement = models.BooleanField(
        verbose_name='согласие на обработку личных данных и '
                     'подтверждение ознакомления с политикой конфиденциальности',
        default=True
    )
    objects = CustomUserManager()

    def clean(self):
        super().clean()
        if self.email and User.objects.exclude(pk=self.pk).filter(
                email__iexact=self.email
        ).exists():
            raise ValidationError('Данный Email уже зарегистрирован.')


class Region(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name_plural = 'Регионы'
        verbose_name = 'Регион'

    def __str__(self):
        return self.name or "unknown region"


class Child(models.Model):
    user_id = models.ForeignKey(
        'User',
        verbose_name='Аккаунт привязки',
        on_delete=models.CASCADE,
        related_name='children',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        validators=[RegexValidator(
            regex='^[а-яА-ЯёЁ-]+$',
            message='Данное поле должно содержать только буквы кириллицы и знак "-"'
        )],
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        validators=[RegexValidator(
            regex='^[а-яА-ЯёЁ-]+$',
            message='Данное поле должно содержать только буквы кириллицы и знак "-"'
        )],
    )

    MALE = 'Мужской'
    FEMALE = 'Женский'
    SEX_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    sex = models.CharField(
        verbose_name='Пол',
        max_length=10,
        choices=SEX_CHOICES,
        default=MALE
    )

    age = models.PositiveIntegerField(
        verbose_name='Возраст',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ],
        error_messages={
            'invalid': 'Поле заполнено не верно'
        }
    )
    region = models.ForeignKey(
        'Region',
        verbose_name='Регион',
        on_delete=models.PROTECT
    )
    school = models.CharField(
        verbose_name='Школа',
        max_length=100,
        validators=[RegexValidator(
            regex='^[а-яА-ЯёЁ0-9№"«» -]+$',
            message='Данное поле должно содержать только кириллицу, числа, "-", №, "", и «»'
        )],
    )
    grade = models.PositiveSmallIntegerField(
        verbose_name='Класс',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )
    attended_speech_therapist = models.BooleanField(
        verbose_name='Посещал ли ребенок раньше логопеда?',
        default=False
    )
    data_processing_agreement = models.BooleanField(
        verbose_name='согласие на обработку личных данных и '
                     'подтверждение ознакомления с политической конфиденциальностью'
    )

    class Meta:
        verbose_name_plural = 'Дети'
        verbose_name = 'Ребенок'


class ChildrenGroup(models.Model):
    user_id = models.ForeignKey(
        'User',
        verbose_name='Аккаунт привязки',
        on_delete=models.CASCADE,
        related_name='children_groups',
    )
    name = models.CharField(
        verbose_name='Название группы',
        max_length=100,
        validators=[RegexValidator(
            regex='^[а-яА-ЯёЁ0-9"«» -]+$',
            message='Данное поле должно содержать только кириллицу, числа, "-", "", и «»'
        )],
    )
    number_of_students = models.PositiveIntegerField(
        verbose_name='Количество учеников в группе',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(50),
        ],
        error_messages={
            'invalid': 'Количество учеников должно быть от 1 до 50'
        }
    )
    average_age = models.DecimalField(
        verbose_name='Средний возраст учеников группы',
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ],
        error_messages={
            'invalid': 'Средний возраст должен быть от 1 до 99'
        }
    )
    region = models.ForeignKey(
        'Region',
        verbose_name='Регион',
        on_delete=models.PROTECT
    )
    school = models.CharField(
        verbose_name='Школа',
        max_length=100,
        validators=[RegexValidator(
            regex='^[а-яА-ЯёЁ0-9№"«» -]+$',
            message='Данное поле должно содержать только кириллицу, числа, "-", №, "", и «»'
        )],
    )

    class Meta:
        verbose_name_plural = 'Группы детей'
        verbose_name = 'Группа детей'
