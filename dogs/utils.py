from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def send_email(subject, message, recipient_list):
    """
    Отправляет электронное письмо.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

# Проверяем роль пользователя
def is_moderator(user):
    return user.role in ['admin', 'moderator']