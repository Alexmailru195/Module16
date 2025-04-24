from django.urls import path
from . import views
from .views import (
    DogListView,
    dog_detail,
    dog_create,
    dog_update,
    dog_delete,
    clear_dog_cache_view,
    clear_all_cache_view,
)

urlpatterns = [
    # Список собак (Class-Based View)
    path(
        '',
        DogListView.as_view(),
        name='dog_list'
    ),

    # Детальная информация о собаке
    path(
        '<int:pk>/',
        dog_detail,
        name='dog_detail'
    ),

    # Создание новой собаки
    path(
        'create/',
        dog_create,
        name='dog_create'
    ),

    # Редактирование информации о собаке
    path(
        '<int:pk>/update/',
        dog_update,
        name='dog_update'
    ),

    # Удаление собаки
    path(
        '<int:pk>/delete/',
        dog_delete,
        name='dog_delete'
    ),

    # Очистка кэша для конкретной собаки
    path(
        '<int:pk>/clear-cache/',
        clear_dog_cache_view,
        name='clear_dog_cache'
    ),

    # Очистка всего кэша
    path(
        'clear-all-cache/',
        clear_all_cache_view,
        name='clear_all_cache'
    ),
]