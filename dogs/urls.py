# from django.urls import path
# from . import views
#
# urlpatterns = [
#     # Список всех собак
#     path('', views.dog_list, name='dog_list'),
#
#     # Создание новой собаки
#     path('create/', views.dog_create, name='dog_create'),
#
#     # Детали конкретной собаки (просмотр)
#     path('<int:pk>/', views.dog_detail, name='dog_detail'),
#
#     # Обновление информации о собаке
#     path('<int:pk>/update/', views.dog_update, name='dog_update'),
#
#     # Удаление собаки
#     path('<int:pk>/delete/', views.dog_delete, name='dog_delete'),
# ]

from django.urls import path
from .views import (
    DogListView,
    dog_detail,
    dog_create,
    dog_update,
    dog_delete,
)

urlpatterns = [
    # Список собак (CBV)
    path('', DogListView.as_view(), name='dog_list'),

    # Детали собаки
    path('<int:pk>/', dog_detail, name='dog_detail'),

    # Создание собаки
    path('create/', dog_create, name='dog_create'),

    # Редактирование собаки
    path('<int:pk>/update/', dog_update, name='dog_update'),

    # Удаление собаки
    path('<int:pk>/delete/', dog_delete, name='dog_delete'),
]