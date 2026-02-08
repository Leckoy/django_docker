from django import forms
from .models import Purchases
from cook.models import Menu, Ingredient
from .models import Allergy

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
<<<<<<< HEAD



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
   
=======
>>>>>>> origin/Kate
