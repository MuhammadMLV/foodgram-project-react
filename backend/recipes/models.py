from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        unique=True,
        null=True,
        blank=True
    )
    slug = models.CharField(
        'Слаг',
        unique=True,
        max_length=100
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )


class Ingredient(models.Model):
    pass
