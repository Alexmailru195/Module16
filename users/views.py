# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings
#
# from .forms import (
#     CustomUserCreationForm,
#     CustomAuthenticationForm,
#     CustomUserUpdateForm,
#     PasswordChangeForm,
# )
#
# from .models import CustomUser
#
# from .utils import generate_random_password
#
#
# def home(request):
#     """
#     Отображает домашнюю страницу.
#     """
#     return render(request, 'users/home.html')
#
#
# # Регистрация нового пользователя
# def register(request):
#     """
#     Обрабатывает регистрацию нового пользователя.
#     """
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Генерация случайного пароля
#             temp_password = generate_random_password()
#
#             # Создание пользователя
#             user = form.save(commit=False)
#             user.set_password(temp_password)
#             user.save()
#
#             # Отправка письма с временным паролем
#             subject = 'Ваш временный пароль'
#             html_message = render_to_string(
#                 'emails/temp_password_email.html', {'temp_password': temp_password}
#             )
#             plain_message = strip_tags(html_message)
#             send_mail(
#                 subject,
#                 plain_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 html_message=html_message,
#                 fail_silently=False,
#             )
#
#             messages.success(
#                 request,
#                 "Регистрация успешна! Проверьте ваш email для получения временного пароля."
#             )
#             return redirect('login')
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})
#
#
# # Вход пользователя
# def user_login(request):
#     """
#     Обрабатывает вход пользователя в систему.
#     """
#     if request.method == "POST":
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"Добро пожаловать, {username}!")
#                 return redirect('profile')
#             else:
#                 messages.error(request, "Неверное имя пользователя или пароль.")
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})
#
#
# # Просмотр профиля пользователя
# @login_required
# def profile(request):
#     """
#     Отображает информацию о текущем пользователе.
#     """
#     return render(request, 'users/profile.html', {'user': request.user})
#
#
# # Изменение данных аккаунта
# @login_required
# def update_profile(request):
#     """
#     Обрабатывает изменение данных пользователя.
#     """
#     if request.method == "POST":
#         form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Данные успешно обновлены!")
#             return redirect('profile')
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = CustomUserUpdateForm(instance=request.user)
#     return render(request, 'users/update_profile.html', {'form': form})
#
#
# # Смена пароля
# @login_required
# def change_password(request):
#     """
#     Обрабатывает смену пароля пользователя.
#     """
#     if request.method == "POST":
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, "Пароль успешно изменён!")
#             return redirect('profile')
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = PasswordChangeForm(user=request.user)
#     return render(request, 'users/change_password.html', {'form': form})
#
#
# # Выход пользователя
# def user_logout(request):
#     """
#     Обрабатывает выход пользователя из системы.
#     """
#     logout(request)
#     messages.info(request, "Вы успешно вышли из аккаунта.")
#     return redirect('login')
#
#
# # Генерация временного пароля
# def generate_temp_password(request):
#     """
#     Генерирует временный пароль и отправляет его на email пользователя.
#     """
#     User = get_user_model()
#     if request.method == "POST":
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, "Пользователь с таким email не найден.")
#             return redirect('generate_temp_password')
#
#         # Генерация случайного пароля
#         temp_password = generate_random_password()
#
#         # Устанавливаем новый пароль
#         user.set_password(temp_password)
#         user.save()
#
#         # Отправляем письмо с временным паролем
#         subject = 'Ваш временный пароль'
#         html_message = render_to_string(
#             'emails/temp_password_email.html', {'temp_password': temp_password}
#         )
#         plain_message = strip_tags(html_message)  # Преобразуем HTML в текст
#         send_mail(
#             subject,
#             plain_message,
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             html_message=html_message,
#             fail_silently=False,
#         )
#
#         messages.success(request, "Временный пароль отправлен на ваш email.")
#         return redirect('login')
#
#     return render(request, 'users/generate_temp_password.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdateForm,
    PasswordChangeForm,
)

from .utils import generate_random_password


def home(request):
    """
    Отображает домашнюю страницу.
    """
    return render(request, 'users/home.html')


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


def register(request):
    """
    Обрабатывает регистрацию нового пользователя.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Генерация случайного пароля
            temp_password = generate_random_password()

            # Создание пользователя
            user = form.save(commit=False)
            user.set_password(temp_password)
            user.save()

            # Отправка письма с временным паролем
            subject = 'Ваш временный пароль'
            html_message = render_to_string(
                'emails/temp_password_email.html', {'temp_password': temp_password}
            )
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(
                request,
                "Регистрация успешна! Проверьте ваш email для получения временного пароля."
            )
            return redirect('login')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """
    Обрабатывает вход пользователя в систему.
    """
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Добро пожаловать, {username}!")
                return redirect('profile')
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    """
    Отображает информацию о текущем пользователе.
    """
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def update_profile(request):
    """
    Обрабатывает изменение данных пользователя.
    """
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные успешно обновлены!")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})


@login_required
def change_password(request):
    """
    Обрабатывает смену пароля пользователя.
    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Пароль успешно изменён!")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


def user_logout(request):
    """
    Обрабатывает выход пользователя из системы.
    """
    logout(request)
    messages.info(request, "Вы успешно вышли из аккаунта.")
    return redirect('login')


def generate_temp_password(request):
    """
    Генерирует временный пароль и отправляет его на email пользователя.
    """
    User = get_user_model()
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
            return redirect('generate_temp_password')

        # Генерация случайного пароля
        temp_password = generate_random_password()

        # Устанавливаем новый пароль
        user.set_password(temp_password)
        user.save()

        # Отправляем письмо с временным паролем
        subject = 'Ваш временный пароль'
        html_message = render_to_string(
            'emails/temp_password_email.html', {'temp_password': temp_password}
        )
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(request, "Временный пароль отправлен на ваш email.")
        return redirect('login')

    return render(request, 'users/generate_temp_password.html')