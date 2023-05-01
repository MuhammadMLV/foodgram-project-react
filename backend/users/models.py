from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def __str__(self):
        return f'{self.username} - {self.email}'


class Subscription(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        to=CustomUser,
        related_name='subscribers',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Подписчик',
        to=CustomUser,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    subs_date = models.DateTimeField(
        'Дата подписки',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('subs_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_author_user'
            )
        ]

    def __str__(self):
        return f'{self.user.username} => {self.author.username}'
