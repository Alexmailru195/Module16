from django.shortcuts import get_object_or_404, render, redirect
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
from django import forms



class DogListView(ListView):
    """
    Отображает список собак с возможностью фильтрации по статусу.
    Администраторы и модераторы могут видеть активных и деактивированных собак.
    """
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'

    def get_queryset(self):
        # Получаем параметр status из GET-запроса
        status = self.request.GET.get('status', 'active')  # По умолчанию показываем активных собак

        # Фильтруем собак в зависимости от статуса
        if self.request.user.role in ['admin', 'moderator']:
            # Администраторы и модераторы могут видеть все собаки
            if status == 'inactive':
                return Dog.objects.filter(is_active=False).select_related('owner', 'breed')
            return Dog.objects.filter(is_active=True).select_related('owner', 'breed')
        else:
            # Обычные пользователи видят только активных собак
            return Dog.objects.filter(is_active=True).select_related('owner', 'breed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем текущий статус в контекст для использования в шаблоне
        context['current_status'] = self.request.GET.get('status', 'active')
        # Добавляем список разрешенных ролей для проверки в шаблоне
        context['allowed_roles'] = ['admin', 'moderator']
        return context


class DogDetailView(DetailView):
    """
    Отображает детальную информацию о собаке с использованием кэширования.
    Увеличивает счетчик просмотров, если пользователь не является владельцем собаки.
    """
    model = Dog
    template_name = 'dogs/dog_detail.html'
    context_object_name = 'dog'

    def get_object(self, queryset=None):
        """
        Получает объект собаки из кэша или базы данных.
        Проверяет активность собаки и права доступа пользователя.
        """
        pk = self.kwargs.get('pk')
        dog = get_dog_from_cache(pk)

        if not dog:
            # Если собака не найдена в кэше, загружаем её из базы данных
            dog = get_object_or_404(Dog, pk=pk)

        # Проверяем, активна ли собака, и имеет ли пользователь доступ
        if not dog.is_active and self.request.user.role not in ['admin', 'moderator']:
            return render(self.request, 'dogs/dog_not_found.html')

        # Увеличиваем счетчик просмотров, если пользователь не владелец
        if self.request.user != dog.owner:
            dog.views_count += 1
            dog.save()

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

class DogFullForm(forms.ModelForm):
    """
    Форма для полного редактирования данных о собаке.
    Включает все поля модели Dog.
    """
    class Meta:
        model = Dog
        fields = '__all__'  # Все поля модели Dog будут доступны в форме

class DogLimitedForm(forms.ModelForm):
    """
    Форма с ограниченным набором полей.
    """
    class Meta:
        model = Dog
        exclude = ('is_active', 'owner', 'views_count')  # Исключаем поля

class DogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Обрабатывает обновление информации о собаке.
    Владелец, администратор или модератор могут редактировать собаку.
    """
    model = Dog
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_form_class(self):
        """
        Возвращает форму в зависимости от уровня доступа пользователя.
        """
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            # Полный доступ для администратора или владельца
            return DogFullForm
        else:
            # Ограниченный доступ для остальных пользователей (например, модераторов)
            return DogLimitedForm

    def get_context_data(self, **kwargs):
        """
        Добавляет inline formset для родословной в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)

        # Создаем inline formset для модели Pedigree
        PedigreeFormSet = inlineformset_factory(
            Dog, Pedigree, form=PedigreeForm, extra=1, can_delete=False, fk_name='dog'
        )

        if self.request.POST:
            context['pedigree_formset'] = PedigreeFormSet(self.request.POST, instance=self.object)
        else:
            context['pedigree_formset'] = PedigreeFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        """
        Проверяет валидность основной формы и inline formset.
        """
        context = self.get_context_data()
        pedigree_formset = context['pedigree_formset']

        if pedigree_formset.is_valid():
            # Сохраняем основную форму и inline formset
            response = super().form_valid(form)
            pedigree_formset.save()
            messages.success(self.request, "Информация о собаке успешно обновлена!")
            return response
        else:
            messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
            return self.form_invalid(form)

    def test_func(self):
        """
        Проверяет права доступа пользователя для редактирования собаки.
        """
        dog = self.get_object()
        user = self.request.user

        # Разрешаем редактирование владельцу, администратору или модератору
        return (
            dog.owner == user or
            user.is_superuser or
            getattr(user, 'role', None) in ['admin', 'moderator']
        )


class DogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Обрабатывает удаление собаки.
    Владелец, администратор или модератор могут удалить собаку.
    """
    model = Dog
    template_name = 'dogs/dog_confirm_delete.html'
    success_url = reverse_lazy('dog_list')

    def test_func(self):
        dog = self.get_object()
        return (
            dog.owner == self.request.user or
            self.request.user.role in ['admin', 'moderator']
        )

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


class ToggleDogStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Класс для изменения статуса активности собаки.
    Доступ разрешен только администраторам и модераторам.
    """

    def test_func(self):
        # Проверяем, является ли пользователь администратором или модератором
        return self.request.user.role in ['admin', 'moderator']

    def get(self, request, pk):
        # Получаем объект собаки по ID
        dog = get_object_or_404(Dog, pk=pk)

        # Инвертируем статус активности
        dog.is_active = not dog.is_active
        dog.save()

        # Добавляем сообщение об успехе
        messages.success(request, f'Статус собаки "{dog.name}" изменен.')

        # Перенаправляем пользователя на страницу списка собак
        return redirect('dog_list')

