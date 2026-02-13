from django import forms
from .models import Purchases, Allergy, Student
from cook.models import Menu, Ingredient
from decimal import Decimal
from django.core.validators import MinValueValidator

class StudentOrderForm(forms.ModelForm):
    FOOD_CHOICES = [
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
    ]
    
    food_intake = forms.ChoiceField(
        choices=FOOD_CHOICES, 
        label="Выберите прием пищи",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_of_meal = forms.DateField(
        label="Дата заказа",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        error_messages={
                'invalid': 'Введите корректную дату',
                }
    )

    class Meta:
        model = Purchases
        fields = [ 'date_of_meal', 'food_intake']


class FeedBackForm(forms.Form):
    mark = forms.ChoiceField(
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        label="Оценка",
        widget=forms.Select(attrs={
            'id': 'score',
            'class': 'form-control'
        })
    )
    
    comment = forms.CharField(
        label="Оставьте свой комментарий",
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'comment',
            'class': 'form-control',
            'placeholder': 'Введите ваш комментарий...'
        }),
        max_length=500,
        required=False
    )


class AddAllergyForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        label="Выберите аллерген",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выберите ингредиент"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].label_from_instance = lambda obj: obj.title

    class Meta:
        model = Allergy
        fields = ["ingredient"]

class TopUpForm(forms.Form):
    requisites = forms.IntegerField(
        label="реквизиты",
        validators=[MinValueValidator(1000000000000000)],
        widget=forms.NumberInput(
            attrs={
                'type': 'int', 
                'class': 'form-control',
                'placeholder': 'Введите 16 цифр карты',
                'pattern': '[0-9]{16}',
                'maxlength': '16'
                }),
    error_messages={
        'required': 'Введите номер карты',
        'invalid': 'Введите 16 цифр (только числа)',
        'min_value': 'Номер карты должен содержать 16 цифр'
    }
    )

    summa = forms.DecimalField(
        label="Сумма пополнения",
        min_value=Decimal('0.01'),
        max_value=Decimal('100000'),
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите сумму пополнения',
                'min': '0.01',
                'step': '0.01'
                }),
        error_messages={
            'min_value': 'Сумма должна быть больше 0',
            'required': 'Введите сумму пополнения',
            'invalid': 'Введите корректную сумму',
            'min_value': 'Сумма слишком большая'
        }
    )

