from django.urls import path
from . import views

urlpatterns = [
    path('', views.dog_list, name='dog_list'),
    path('<int:pk>/', views.dog_detail, name='dog_detail'),
    path('new/', views.dog_create, name='dog_create'),
    path('<int:pk>/edit/', views.dog_update, name='dog_update'),
    path('<int:pk>/delete/', views.dog_delete, name='dog_delete'),
]