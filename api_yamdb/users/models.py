from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from .validators import validate_username

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

LIST_OF_ROLES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
]


class User(AbstractUser):
    """
    Модель для управления пользователями. Модель расширена полями с биографией,
    ролью (админ, модератор, пользователь) и подтверждающим кодом.
    """
    username = models.CharField(
        validators=(validate_username,),
        max_length=120,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Никнейм'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email'
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=LIST_OF_ROLES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        null=True,
        blank=False,
        default='null'
    )

    """
    Проверка на наличие роли в базе данных.
    """

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user')
        ]
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
