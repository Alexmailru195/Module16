from django.core.cache import cache

def get_dog_from_cache(dog_id):
    """
    Получает данные о собаке из кэша.
    Если данных нет в кэше, загружает их из базы данных и сохраняет в кэш.
    """
    key = f'dog_{dog_id}'
    dog = cache.get(key)

    if not dog:
        from .models import Dog
        try:
            dog = Dog.objects.select_related('breed', 'owner').get(id=dog_id)
            cache.set(key, dog, timeout=600)
        except Dog.DoesNotExist:
            return None

    return dog


def clear_dog_cache(dog_id):
    """
    Очищает кэш для конкретной собаки.
    """
    key = f'dog_{dog_id}'
    cache.delete(key)


def clear_all_cache():
    """
    Очищает весь кэш.
    """
    cache.clear()