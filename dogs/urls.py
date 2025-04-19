from django.urls import path
from .views import (
    DogListView,
    dog_detail,
    dog_create,
    dog_update,
    dog_delete,
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
]