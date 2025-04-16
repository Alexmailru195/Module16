from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dog
from .forms import DogForm


# Список всех собак
def dog_list(request):
    """
    Отображает список всех собак.
    """
    dogs = Dog.objects.all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})


# Детали собаки
def dog_detail(request, pk):
    """
    Отображает детальную информацию о собаке.
    """
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dogs/dog_detail.html', {'dog': dog})


# Создание новой собаки
@login_required
def dog_create(request):
    """
    Обрабатывает создание новой собаки.
    """
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)  # Не сохраняем форму сразу
            dog.owner = request.user  # Устанавливаем владельца как текущего пользователя
            dog.save()  # Сохраняем объект в базе данных
            messages.success(request, "Собака успешно добавлена!")
            return redirect('dog_list')  # Перенаправление на список собак
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = DogForm()
    return render(request, 'dogs/dog_form.html', {'form': form})


# Обновление информации о собаке
@login_required
def dog_update(request, pk):
    """
    Обрабатывает обновление информации о собаке.
    Только владелец может редактировать свою собаку.
    """
    dog = get_object_or_404(Dog, pk=pk)

    # Проверка, является ли текущий пользователь владельцем собаки
    if dog.owner != request.user:
        messages.error(request, "У вас нет прав для редактирования этой собаки.")
        return redirect('dog_list')

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, "Информация о собаке успешно обновлена!")
            return redirect('dog_detail', pk=dog.pk)  # Перенаправление на детали собаки
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = DogForm(instance=dog)
    return render(request, 'dogs/dog_form.html', {'form': form})


# Удаление собаки
@login_required
def dog_delete(request, pk):
    """
    Обрабатывает удаление собаки.
    Только владелец может удалить свою собаку.
    """
    dog = get_object_or_404(Dog, pk=pk)

    # Проверка, является ли текущий пользователь владельцем собаки
    if dog.owner != request.user:
        messages.error(request, "У вас нет прав для удаления этой собаки.")
        return redirect('dog_list')

    if request.method == "POST":
        dog.delete()
        messages.success(request, "Собака успешно удалена!")
        return redirect('dog_list')  # Перенаправление на список собак

    return render(request, 'dogs/dog_confirm_delete.html', {'dog': dog})