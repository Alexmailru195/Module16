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
from django.views.generic import View, TemplateView, FormView, CreateView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdateForm,
)
from .models import Dog
from .utils import generate_random_password


class HomeView(TemplateView):
    """
    Отображает домашнюю страницу.
    """
    template_name = 'users/home.html'


class UserCreateView(CreateView):
    """
    Регистрация нового пользователя.
    """
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
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
            self.request,
            "Регистрация успешна! Проверьте ваш email для получения временного пароля."
        )
        return super().form_valid(form)


class UserLoginView(FormView):
    """
    Вход пользователя в систему.
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"Добро пожаловать, {username}!")
            return redirect('profile')
        else:
            messages.error(self.request, "Неверное имя пользователя или пароль.")
            return redirect('login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Отображает информацию о текущем пользователе.
    """
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UpdateProfileView(LoginRequiredMixin, FormView):
    """
    Обрабатывает изменение данных пользователя.
    """
    form_class = CustomUserUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Данные успешно обновлены!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
        return super().form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    """
    Обрабатывает смену пароля пользователя.
    """
    form_class = PasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Пароль успешно изменён!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
        return super().form_invalid(form)


class UserLogoutView(View):
    """
    Обрабатывает выход пользователя из системы.
    """
    def get(self, request):
        logout(request)
        messages.info(request, "Вы успешно вышли из аккаунта.")
        return redirect('login')


class GenerateTempPasswordView(View):
    """
    Генерирует временный пароль и отправляет его на email пользователя.
    """
    template_name = 'users/generate_temp_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        User = get_user_model()
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


class MyDogsView(LoginRequiredMixin, TemplateView):
    """
    Отображает список собак текущего пользователя.
    """
    template_name = 'users/my_dogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['dogs'] = user.dogs.all()
        return context