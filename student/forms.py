from django import forms
from .models import Purchases
from cook.models import Menu

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
        