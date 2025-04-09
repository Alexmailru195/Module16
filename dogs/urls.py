from django.urls import path
from . import views

urlpatterns = [
    path('', views.dog_list, name='dog_list'),  # Список собак
    path('create/', views.dog_create, name='dog_create'),  # Создание собаки
    path('<int:pk>/', views.dog_detail, name='dog_detail'),  # Детали собаки
    path('<int:pk>/update/', views.dog_update, name='dog_update'),  # Изменение собаки
    path('<int:pk>/delete/', views.dog_delete, name='dog_delete'),  # Удаление собаки
]