from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random
import string


def generate_random_slug(length=8):
    """
    Генерирует случайный slug заданной длины.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True
    )
    email = models.EmailField(
        unique=True
    )
    slug = models.SlugField(
        unique=True, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        """
        Автоматически генерирует slug, если он не был указан.
        """
        if not self.slug:
            # Генерируем уникальный slug
            while True:
                new_slug = generate_random_slug()
                if not CustomUser.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dogs_users',
        verbose_name="Владелец"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"


class Review(models.Model):
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_reviews',
        verbose_name="Автор отзыва"
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name="Целевой пользователь"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        choices=[(i, i) for i in range(1, 6)]
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус отзыва"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def approve(self):
        """Одобрение отзыва и отправка уведомления автору."""
        self.status = 'approved'
        self.save()
        self.send_approval_notification()

    def reject(self):
        """Отклонение отзыва."""
        self.status = 'rejected'
        self.save()

    def send_approval_notification(self):
        """Отправка уведомления автору отзыва о его одобрении."""
        subject = 'Ваш отзыв был одобрен!'
        html_message = render_to_string('emails/review_approved_email.html', {'review': self})
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.author.email],
            html_message=html_message,
            fail_silently=False,
        )

    def __str__(self):
        return f"Отзыв от {self.author.username} для {self.target_user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
