from django.urls import path
from . import views

urlpatterns = [
    # Домашняя страница
    path('', views.home, name='home'),

    # Регистрация нового пользователя
    path('register/', views.register, name='register'),

    # Вход в аккаунт
    path('login/', views.user_login, name='login'),

    # Просмотр профиля
    path('profile/', views.profile, name='profile'),

    # Изменение данных аккаунта
    path('update_profile/', views.update_profile, name='update_profile'),

    # Смена пароля
    path('change_password/', views.change_password, name='change_password'),

    # Выход из аккаунта
    path('logout/', views.user_logout, name='logout'),
]