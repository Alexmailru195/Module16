from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date


class Breed(models.Model):
    """
    Модель для породы собаки.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Название породы")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Описание породы")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Порода")
        verbose_name_plural = _("Породы")


class Dog(models.Model):
    """
    Модель для собаки.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Кличка собаки")
    )
    breed = models.ForeignKey(
        'Breed',
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name=_("Порода")
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dogs',
        verbose_name=_("Владелец")
    )
    birth_date = models.DateField(
        verbose_name=_("Дата рождения")
    )
    photo = models.ImageField(
        upload_to='dogs/',
        blank=True,
        null=True,
        verbose_name=_("Фото собаки")
    )

    def clean(self):
        """
        Валидация: дата рождения не может быть в будущем.
        """
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError(_("Дата рождения не может быть в будущем."))

    def age(self):
        """
        Вычисляет возраст собаки в годах на основе даты рождения.
        """
        today = date.today()
        age = today.year - self.birth_date.year
        # Проверяем, прошел ли день рождения в этом году
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def __str__(self):
        return _("{name} ({breed})").format(name=self.name, breed=self.breed)

    class Meta:
        verbose_name = _("Собака")
        verbose_name_plural = _("Собаки")


class Pedigree(models.Model):
    """
    Модель для родословной собаки.
    """
    dog = models.OneToOneField(
        Dog,
        on_delete=models.CASCADE,
        related_name='pedigree'
    )
    father = models.ForeignKey(
        Dog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='father_of'
    )
    mother = models.ForeignKey(
        Dog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mother_of'
    )
    registration_number = models.CharField(
        max_length=50,
        unique=True
    )
    issued_by = models.CharField(
        max_length=100
    )
    issue_date = models.DateField()

    def clean(self):
        """
        Валидация для родословной:
        1. Собака не может быть своим же отцом или матерью.
        2. Отец и мать не могут быть одной и той же собакой.
        """
        if self.father == self.dog or self.mother == self.dog:
            raise ValidationError(_("Собака не может быть своим же отцом или матерью."))

        if self.father and self.mother and self.father == self.mother:
            raise ValidationError(_("Отец и мать не могут быть одной и той же собакой."))

    def __str__(self):
        return f"Родословная {self.dog.name} (№{self.registration_number})"