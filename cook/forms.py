
from django import forms
from .models import Dish
from cook.models import Menu

class CreateMenuForm(forms.ModelForm):
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
    
    date = forms.DateField(
        label="Дата меню",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    dish1 = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо 1",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dish2 = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо 2",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dish3 = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо 3",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dish4 = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо 4",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dish5 = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо 5",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Menu
        fields = ['date', 'food_intake', 'dish1', 'dish2', 'dish3', 'dish4', 'dish5']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['dish1'].queryset = Dish.objects.filter(dish_type=1) # Только супы
        self.fields['dish2'].queryset = Dish.objects.filter(dish_type=2) # Только вторые
        self.fields['dish3'].queryset = Dish.objects.filter(dish_type=3) # Только гарниры
        self.fields['dish4'].queryset = Dish.objects.filter(dish_type=4) # Только салаты
        self.fields['dish5'].queryset = Dish.objects.filter(dish_type=5) # Только напитки