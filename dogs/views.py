from django.shortcuts import get_object_or_404, render, redirect
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
    Отображение списка собак с возможностью:
    Поиска по имени,
    Поиска по породе,
    Сортировки по имени, породе или дате рождения,
    Переключения между активными и деактивированными собаками.
    """
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'
    paginate_by = 2

    def get_queryset(self):
        status = self.request.GET.get('status', 'active')  # По умолчанию показываем активных собак
        breed_search = self.request.GET.get('breed_search', '')  # Параметр для поиска по породе
        search_query = self.request.GET.get('search', '')  # Параметр для поиска по имени
        sort_by = self.request.GET.get('sort_by', 'name')  # Параметр для сортировки (по умолчанию "имя")

        queryset = Dog.objects.all()

        if self.request.user.role in ['admin', 'moderator']:
            if status == 'inactive':
                queryset = queryset.filter(is_active=False)
            else:
                queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=True)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if breed_search:
            queryset = queryset.filter(breed__name__icontains=breed_search)

        if sort_by in ['name', 'breed', 'birth_date']:
            queryset = queryset.order_by(sort_by)

        queryset = queryset.select_related('owner')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_status'] = self.request.GET.get('status', 'active')
        context['allowed_roles'] = ['admin', 'moderator']

        context['breed_search'] = self.request.GET.get('breed_search', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort_by', 'name')

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
        # Получаем параметры из URL
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')

        if not slug and not pk:
            raise ValueError("Необходимо указать либо 'slug', либо 'pk'.")

        dog = get_dog_from_cache(slug=slug, pk=pk)

        if not dog:
            if slug:
                dog = get_object_or_404(Dog, slug=slug)
            elif pk:
                dog = get_object_or_404(Dog, pk=pk)

        if not dog.is_active and self.request.user.role not in ['admin', 'moderator']:
            return render(self.request, 'dogs/dog_not_found.html')

        # Увеличиваем счетчик просмотров, если пользователь не владелец
        if self.request.user != dog.owner:
            dog.views_count += 1
            dog.save()

        return dog


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Обрабатывает создание новой собаки и её родословной
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
            dog = form.save(commit=False)
            dog.owner = self.request.user
            dog.save()

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
        fields = '__all__'

class DogLimitedForm(forms.ModelForm):
    """
    Форма с ограниченным набором полей
    """
    class Meta:
        model = Dog
        exclude = ('is_active', 'owner', 'views_count')

class DogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Обрабатывает обновление информации о собаке
    Владелец, администратор или модератор могут редактировать собаку
    """
    model = Dog
    template_name = 'dogs/dog_form.html'
    success_url = reverse_lazy('dog_list')

    def get_form_class(self):
        """
        Возвращает форму в зависимости от уровня доступа пользователя
        """
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return DogFullForm
        else:
            return DogLimitedForm

    def get_context_data(self, **kwargs):
        """
        Добавляет inline formset для родословной в контекст шаблона
        """
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
        """
        Проверяет валидность основной формы и inline formset
        """
        context = self.get_context_data()
        pedigree_formset = context['pedigree_formset']

        if pedigree_formset.is_valid():
            response = super().form_valid(form)
            pedigree_formset.save()
            messages.success(self.request, "Информация о собаке успешно обновлена!")
            return response
        else:
            messages.error(self.request, "Ошибка в форме. Проверьте введенные данные.")
            return self.form_invalid(form)

    def test_func(self):
        """
        Проверяет права доступа пользователя для редактирования собаки
        """
        dog = self.get_object()
        user = self.request.user

        return (
            dog.owner == user or
            user.is_superuser or
            getattr(user, 'role', None) in ['admin', 'moderator']
        )


class DogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Обрабатывает удаление собаки
    Владелец, администратор или модератор могут удалить собаку
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
    Очищает кэш для конкретной собаки
    """
    def get(self, request, pk):
        clear_dog_cache(pk)
        return JsonResponse({'message': f'Кэш для собаки с ID {pk} очищен.'})


class ClearAllCacheView(View):
    """
    Очищает весь кэш
    """
    def get(self, request):
        clear_all_cache()
        return JsonResponse({'message': 'Весь кэш очищен.'})


class ToggleDogStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Класс для изменения статуса активности собаки
    Доступ разрешен только администраторам и модераторам
    """

    def test_func(self):
        return self.request.user.role in ['admin', 'moderator']

    def get(self, request, pk):
        # Получаем объект собаки по ID
        dog = get_object_or_404(Dog, pk=pk)

        dog.is_active = not dog.is_active
        dog.save()

        messages.success(request, f'Статус собаки "{dog.name}" изменен.')

        return redirect('dog_list')