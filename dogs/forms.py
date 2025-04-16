from django import forms
from .models import Dog
from datetime import date

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'birth_date', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_birth_date(self):
        """
        Валидация даты рождения: проверка, что дата не находится в будущем.
        """
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise forms.ValidationError("Дата рождения не может быть в будущем.")
        return birth_date