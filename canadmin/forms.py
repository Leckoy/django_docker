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
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ingredient name'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in grams'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Cost'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Ingredient Name',
            'amount': 'Amount (g)',
            'cost': 'Cost',
            'picture': 'Picture',
        }

class AddNewDishForm(forms.ModelForm):
    DISH_TYPE_CHOICES = [
        (1, 'soup(1)'),
        (2, 'salad(2)'),
        (3, 'main(3)'),
        (4, 'dessert(4)'),
        (5, 'drink(5)'),
    ]

    dish_type = forms.ChoiceField(
        choices=DISH_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Dish Type'
    )

    class Meta:
        model = Dish
        fields = ['title', 'weight', 'cost', 'dish_type', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dish name'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in grams'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Cost'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Dish Name',
            'weight': 'Weight (g)',
            'cost': 'Cost',
            'picture': 'Picture',
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
