from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Dog, Pedigree
from .forms import DogForm, PedigreeForm
from .services import get_dog_from_cache, clear_dog_cache, clear_all_cache
from .utils import send_email


class DogListView(ListView):
    """
    Отображает список всех собак.
    Авторизованный пользователь видит всех собак.
    """
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'

    def get_queryset(self):
        # Возвращаем всех собак без фильтрации по владельцу
        return Dog.objects.all().select_related('owner', 'breed')


class DogDetailView(DetailView):
    """
    Отображает детальную информацию о собаке с использованием кэширования.
    """
    model = Dog
    template_name = 'dogs/dog_detail.html'
    context_object_name = 'dog'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        dog = get_dog_from_cache(pk)
        if not dog:
            return render(self.request, 'dogs/dog_not_found.html')
        return dog


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Обрабатывает создание новой собаки и её родословной.
    """
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PedigreeFormSet = inlineformset_factory(
            Dog, Pedigree, form=PedigreeForm, extra=1, can_delete=False, fk_name='dog'
        )
        if self.request.POST:
            context['pedigree_formset'] = PedigreeFormSet(self.request.POST)
        else:
            context['pedigree_formset'] = PedigreeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        pedigree_formset = context['pedigree_formset']

        if pedigree_formset.is_valid():
            # Устанавливаем владельца как текущего пользователя
            dog = form.save(commit=False)
            dog.owner = self.request.user
            dog.save()

            # Сохраняем родословную
            pedigree_formset.instance = dog
            pedigree_formset.save()

            # Отправляем уведомление на email пользователя
            subject = "Новая собака зарегистрирована"
            message = f"Вы успешно зарегистрировали собаку: {dog.name}."
            recipient_list = [self.request.user.email]
            send_email(subject, message, recipient_list)

            messages.success(self.request, "Собака успешно добавлена!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
            return self.form_invalid(form)


class DogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Обрабатывает обновление информации о собаке.
    Только владелец может редактировать свою собаку.
    """
    model = Dog
    form_class = DogForm
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PedigreeFormSet = inlineformset_factory(
            Dog, Pedigree, form=PedigreeForm, extra=1, can_delete=False, fk_name='dog'
        )
        if self.request.POST:
            context['pedigree_formset'] = PedigreeFormSet(self.request.POST, instance=self.object)
        else:
            context['pedigree_formset'] = PedigreeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        pedigree_formset = context['pedigree_formset']

        if pedigree_formset.is_valid():
            form.save()
            pedigree_formset.save()
            messages.success(self.request, "Информация о собаке успешно обновлена!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
            return self.form_invalid(form)

    def test_func(self):
        dog = self.get_object()
        return dog.owner == self.request.user


class DogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Обрабатывает удаление собаки.
    Только владелец может удалить свою собаку.
    """
    model = Dog
    template_name = 'dogs/dog_confirm_delete.html'
    success_url = reverse_lazy('dog_list')

    def test_func(self):
        dog = self.get_object()
        return dog.owner == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Собака успешно удалена!")
        return super().delete(request, *args, **kwargs)


class ClearDogCacheView(View):
    """
    Очищает кэш для конкретной собаки.
    """
    def get(self, request, pk):
        clear_dog_cache(pk)
        return JsonResponse({'message': f'Кэш для собаки с ID {pk} очищен.'})


class ClearAllCacheView(View):
    """
    Очищает весь кэш.
    """
    def get(self, request):
        clear_all_cache()
        return JsonResponse({'message': 'Весь кэш очищен.'})