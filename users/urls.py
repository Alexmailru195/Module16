from django.urls import path
from .views import (
    HomeView,
    UserCreateView,
    UserLoginView,
    ProfileView,
    MyDogsView,
    UpdateProfileView,
    ChangePasswordView,
    UserLogoutView,
    GenerateTempPasswordView,
)

urlpatterns = [
    # Домашняя страница
    path('', HomeView.as_view(), name='home'),

    # Регистрация нового пользователя
    path('register/', UserCreateView.as_view(), name='register'),

    # Вход в аккаунт
    path('login/', UserLoginView.as_view(), name='login'),

    # Просмотр профиля
    path('profile/', ProfileView.as_view(), name='profile'),

    # Список собак пользователя
    path('my-dogs/', MyDogsView.as_view(), name='my_dogs'),

    # Изменение данных аккаунта
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),

    # Смена пароля
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Выход из аккаунта
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Генерация временного пароля (восстановление доступа)
    path('generate-temp-password/', GenerateTempPasswordView.as_view(), name='generate_temp_password'),
]