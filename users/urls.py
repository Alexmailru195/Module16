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
    path('update-profile/', views.update_profile, name='update_profile'),

    # Смена пароля
    path('change-password/', views.change_password, name='change_password'),

    # Выход из аккаунта
    path('logout/', views.user_logout, name='logout'),

    # Генерация временного пароля (восстановление доступа)
    path('generate-temp-password/', views.generate_temp_password, name='generate_temp_password'),
]