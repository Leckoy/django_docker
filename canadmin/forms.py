from django import forms
from main.models import User, Role
from django.contrib.auth import authenticate
from student.models import Student
from cook.models import Dish, Ingredient, Composition
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError




class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['name', 'login', 'role']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if user.role_id == 2: 
                Student.objects.create(
                    user=user,
                    money=0
                )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['role'].queryset = Role.objects.filter(title="Student")
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'password1':
                field.widget.attrs['class'] += ' password-field'

class IngredAddForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['title', 'amount', 'cost', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название ингредиента'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма в граммах'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Цена'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название ингредиента',
            'amount': 'Сумма (г)',
            'cost': 'Цена',
            'picture': 'Изображение',
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if Ingredient.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError("Ингредиент с таким названием уже существует.")
        return title


class AddNewDishForm(forms.ModelForm):
    DISH_TYPE_CHOICES = [
        (1, 'суп(1)'),
        (2, 'салат(2)'),
        (3, 'главное блюдо(3)'),
        (4, 'десерт(4)'),
        (5, 'напиток(5)'),
    ]

    dish_type = forms.ChoiceField(
        choices=DISH_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип блюда'
    )

    class Meta:
        model = Dish
        fields = ['title', 'weight', 'cost', 'dish_type', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название блюда'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Вес в граммах'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Цена'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название блюда',
            'weight': 'Вес (г)',
            'cost': 'Цена',
            'picture': 'Изображение',
        }

        error_messages = {
            'title': {
                'required': 'Введите название блюда.',
            },
            'weight': {
                'required': 'Укажите вес блюда',
                'invalid': 'Введите корректное число',
                'min_value': 'Вес должен быть больше 0',
            },
            'cost': {
                'required': 'Укажите стоимость блюда',
                'invalid': 'Введите корректную цену',
                'min_value': 'Цена должна быть больше 0',
            },
            'picture': {
                'required': 'Загрузите изображение блюда',
                'invalid': 'Загрузите корректный файл изображения',
            },
        }

class CompositionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        dish_weight = self.instance.weight
        total_weight = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                ingr_weight = form.cleaned_data.get('weight', 0)
                if ingr_weight > dish_weight:
                    form.add_error('weight', f"Вес ингредиента ({ingr_weight} г) не может превышать вес блюда ({dish_weight} г).")
                total_weight += ingr_weight

        if total_weight > dish_weight:
            raise ValidationError(f"Суммарный вес ингредиентов ({total_weight} г) превышает вес блюда ({dish_weight} г).")

CompositionFormSet = inlineformset_factory(
    Dish,
    Composition,
    fields=['ingredient', 'weight'],
    extra=5,
    formset=CompositionInlineFormSet

)
