from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm, PasswordChangeForm

# Главная страница
def home(request):
    """
    Отображает домашнюю страницу.
    """
    return render(request, 'users/home.html')

# Регистрация нового пользователя
def register(request):
    """
    Обрабатывает регистрацию нового пользователя.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, "Регистрация успешна!")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Вход пользователя
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

# Просмотр профиля пользователя
@login_required
def profile(request):
    """
    Отображает информацию о текущем пользователе.
    """
    return render(request, 'users/profile.html', {'user': request.user})

# Изменение данных аккаунта
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

# Смена пароля
@login_required
def change_password(request):
    """
    Обрабатывает смену пароля пользователя.
    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Обновляем сессию после смены пароля
            messages.success(request, "Пароль успешно изменён!")
            return redirect('profile')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

# Выход пользователя
def user_logout(request):
    """
    Обрабатывает выход пользователя из системы.
    """
    logout(request)
    messages.info(request, "Вы успешно вышли из аккаунта.")
    return redirect('login')