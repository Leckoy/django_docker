
from django import forms
from .models import Dish
from cook.models import Menu, Ingredient

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




class IngredientUseForm(forms.ModelForm):
    title = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        label="Ингредиент",
        to_field_name = "title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'ingredients_datalist',
            'autocomplete': 'off'
        })
    )

    amount = forms.FloatField(
        label="Количество использованных ингредиетов",
        widget=forms.NumberInput(attrs={'type': 'int', 'class': 'form-control'})
    )

    class Meta:
        model = Ingredient
        fields = ['title', 'amount']



class DishAddForm(forms.ModelForm):
    title = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label="Блюдо",
        to_field_name = "title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'dish_datalist',
            'autocomplete': 'off'
        })
    )

    weigh = forms.FloatField(
        label="Количество блюд ддля добавления",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'step': '0.01'
        })
    )
    class Meta:
        model = Dish
        fields = ['title', 'weigh']



class IngredientOrdeForm(forms.ModelForm):
    title = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        label="Ингредиент",
        to_field_name = "title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'ingredients_datalist',
            'autocomplete': 'off'
        })
    )

    amount = forms.FloatField(
        label="Количество заказанных ингредиетов",
        widget=forms.NumberInput(attrs={'type': 'int', 'class': 'form-control'})
    )

    class Meta:
        model = Ingredient
        fields = ['title', 'amount']