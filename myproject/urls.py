from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Маршрут для админки Django
    path('admin/', admin.site.urls),

    # Маршруты для приложения users (корневой маршрут)
    path('', include('users.urls')),  # Корневой маршрут для пользователей

    # Маршруты для приложения dogs
    path('dogs/', include('dogs.urls')),  # Маршруты для собак
]

# Добавляем обработку медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)