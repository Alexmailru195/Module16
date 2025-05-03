from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с дополнительными полями.
    """
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Адрес"
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Dog(models.Model):
    """
    Модель для хранения информации о собаках.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Имя собаки"
    )
    breed = models.CharField(
        max_length=100,
        verbose_name="Порода"
    )
    age = models.PositiveIntegerField(
        verbose_name="Возраст"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='dogs_users',
        verbose_name="Владелец"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"