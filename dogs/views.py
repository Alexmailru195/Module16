# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Dog
# from .forms import DogForm
#
#
# # Список всех собак
# def dog_list(request):
#     """
#     Отображает список всех собак.
#     """
#     dogs = Dog.objects.all()
#     return render(request, 'dogs/dog_list.html', {'dogs': dogs})
#
#
# # Детали собаки
# def dog_detail(request, pk):
#     """
#     Отображает детальную информацию о собаке.
#     """
#     dog = get_object_or_404(Dog, pk=pk)
#     return render(request, 'dogs/dog_detail.html', {'dog': dog})
#
#
# # Создание новой собаки
# @login_required
# def dog_create(request):
#     """
#     Обрабатывает создание новой собаки.
#     """
#     if request.method == "POST":
#         form = DogForm(request.POST, request.FILES)
#         if form.is_valid():
#             dog = form.save(commit=False)  # Не сохраняем форму сразу
#             dog.owner = request.user  # Устанавливаем владельца как текущего пользователя
#             dog.save()  # Сохраняем объект в базе данных
#             messages.success(request, "Собака успешно добавлена!")
#             return redirect('dog_list')  # Перенаправление на список собак
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = DogForm()
#     return render(request, 'dogs/dog_form.html', {'form': form})
#
#
# # Обновление информации о собаке
# @login_required
# def dog_update(request, pk):
#     """
#     Обрабатывает обновление информации о собаке.
#     Только владелец может редактировать свою собаку.
#     """
#     dog = get_object_or_404(Dog, pk=pk)
#
#     # Проверка, является ли текущий пользователь владельцем собаки
#     if dog.owner != request.user:
#         messages.error(request, "У вас нет прав для редактирования этой собаки.")
#         return redirect('dog_list')
#
#     if request.method == "POST":
#         form = DogForm(request.POST, request.FILES, instance=dog)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Информация о собаке успешно обновлена!")
#             return redirect('dog_detail', pk=dog.pk)  # Перенаправление на детали собаки
#         else:
#             messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
#     else:
#         form = DogForm(instance=dog)
#     return render(request, 'dogs/dog_form.html', {'form': form})
#
#
# # Удаление собаки
# @login_required
# def dog_delete(request, pk):
#     """
#     Обрабатывает удаление собаки.
#     Только владелец может удалить свою собаку.
#     """
#     dog = get_object_or_404(Dog, pk=pk)
#
#     # Проверка, является ли текущий пользователь владельцем собаки
#     if dog.owner != request.user:
#         messages.error(request, "У вас нет прав для удаления этой собаки.")
#         return redirect('dog_list')
#
#     if request.method == "POST":
#         dog.delete()
#         messages.success(request, "Собака успешно удалена!")
#         return redirect('dog_list')  # Перенаправление на список собак
#
#     return render(request, 'dogs/dog_confirm_delete.html', {'dog': dog})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.forms import inlineformset_factory
from django.http import JsonResponse
from .models import Dog, Pedigree
from .forms import DogForm, PedigreeForm
from .services import get_dog_from_cache, clear_dog_cache, clear_all_cache
from .utils import send_email


class DogListView(ListView):
    """
    Отображает список всех собак.
    Если пользователь авторизован, отображаются только его собаки.
    """
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'

    def get_queryset(self):
        return Dog.objects.all().select_related('owner', 'breed')

def dog_detail(request, pk):
    """
    Отображает детальную информацию о собаке с использованием кэширования.
    """
    dog = get_dog_from_cache(pk)
    if not dog:
        return render(request, 'dogs/dog_not_found.html')

    return render(request, 'dogs/dog_detail.html', {'dog': dog})


@login_required
def dog_create(request):
    """
    Обрабатывает создание новой собаки и её родословной.
    """
    PedigreeFormSet = inlineformset_factory(
        Dog, Pedigree, form=PedigreeForm, extra=1, can_delete=False, fk_name='dog'
    )

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES)
        pedigree_formset = PedigreeFormSet(request.POST, instance=Dog())

        if form.is_valid() and pedigree_formset.is_valid():
            dog = form.save(commit=False)
            dog.owner = request.user  # Устанавливаем владельца как текущего пользователя
            dog.save()  # Сохраняем объект в базе данных

            pedigree_formset.instance = dog
            pedigree_formset.save()

            # Отправляем уведомление на email пользователя
            subject = "Новая собака зарегистрирована"
            message = f"Вы успешно зарегистрировали собаку: {dog.name}."
            recipient_list = [request.user.email]
            send_email(subject, message, recipient_list)

            messages.success(request, "Собака успешно добавлена!")
            return redirect('dog_list')
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = DogForm()
        pedigree_formset = PedigreeFormSet(instance=Dog())

    return render(request, 'dogs/dog_form.html', {
        'form': form,
        'pedigree_formset': pedigree_formset,
    })


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

    PedigreeFormSet = inlineformset_factory(
        Dog, Pedigree, form=PedigreeForm, extra=1, can_delete=False, fk_name='dog'
    )

    if request.method == "POST":
        form = DogForm(request.POST, request.FILES, instance=dog)
        pedigree_formset = PedigreeFormSet(request.POST, instance=dog)

        if form.is_valid() and pedigree_formset.is_valid():
            form.save()
            pedigree_formset.save()
            messages.success(request, "Информация о собаке успешно обновлена!")
            return redirect('dog_detail', pk=dog.pk)
        else:
            messages.error(request, "Ошибка в форме. Проверьте введенные данные.")
    else:
        form = DogForm(instance=dog)
        pedigree_formset = PedigreeFormSet(instance=dog)

    return render(request, 'dogs/dog_form.html', {
        'form': form,
        'pedigree_formset': pedigree_formset,
    })


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
        return redirect('dog_list')

    return render(request, 'dogs/dog_confirm_delete.html', {'dog': dog})


def clear_dog_cache_view(request, pk):
    """
    Очищает кэш для конкретной собаки.
    """
    clear_dog_cache(pk)
    return JsonResponse({'message': f'Кэш для собаки с ID {pk} очищен.'})


def clear_all_cache_view(request):
    """
    Очищает весь кэш.
    """
    clear_all_cache()
    return JsonResponse({'message': 'Весь кэш очищен.'})