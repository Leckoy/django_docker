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

