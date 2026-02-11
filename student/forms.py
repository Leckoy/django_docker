from django import forms
from .models import Purchases, Student
from cook.models import Menu, Ingredient
from .models import Allergy
from decimal import Decimal

class BuyAbonimentForm(forms.Form):
    choise = forms.ChoiceField(
        choices = [
            ('7', 'Неделя — 5000 руб.'),
            ('14', '2 недели — 10000 руб.'),
            ('30', 'Месяц — 20000 руб.'),
            ('90', '3 месяца — 60000 руб.'),
            ('180', '6 месяцев — 120000 руб.'),
            ('270', '9 месяцев — 150000 руб.'),
        ],
        label="План абонемента",
        widget=forms.Select(attrs={
            'id': 'plan',
            'class': 'form-control'
        })
    )


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
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
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

