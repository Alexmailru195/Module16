from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dog
from .forms import DogForm

# Список всех собак
def dog_list(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/dog_list.html', {'dogs': dogs})

# Детали собаки
def dog_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dogs/dog_detail.html', {'dog': dog})

# Создание новой собаки
@login_required
def dog_create(request):
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)  # Не сохраняем форму сразу
            dog.owner = request.user  # Устанавливаем владельца как текущего пользователя
            dog.save()  # Сохраняем объект в базе данных
            messages.success(request, "Собака успешно добавлена!")
            return redirect('dog_list')  # Перенаправление на список собак
    else:
        form = DogForm()
    return render(request, 'dogs/dog_form.html', {'form': form})

# Обновление информации о собаке
@login_required
def dog_update(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, "Информация о собаке успешно обновлена!")
            return redirect('dog_detail', pk=dog.pk)  # Перенаправление на детали собаки
    else:
        form = DogForm(instance=dog)
    return render(request, 'dogs/dog_form.html', {'form': form})

# Удаление собаки
@login_required
def dog_delete(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if request.method == "POST":
        dog.delete()
        messages.success(request, "Собака успешно удалена!")
        return redirect('dog_list')  # Перенаправление на список собак
    return render(request, 'dogs/dog_confirm_delete.html', {'dog': dog})