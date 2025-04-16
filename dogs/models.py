from django.db import models
from django.conf import settings

class Breed(models.Model):
    """
    Модель для породы собаки.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Название породы"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание породы"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"


class Dog(models.Model):
    """
    Модель для собаки.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Кличка собаки"
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name="Порода"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name="Владелец"
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения"
    )
    photo = models.ImageField(
        upload_to='dogs/',
        blank=True,
        null=True,
        verbose_name="Фото собаки"
    )

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"