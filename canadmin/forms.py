from django import forms
from main.models import User, Role
from django.contrib.auth import authenticate
from student.models import Student
from cook.models import Dish, Ingredient


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
# class AddNewDishForm(forms.ModelForm):
#     title = forms.CharField(max_length=255)
#     weight = forms.FloatField(label="Вес (г)")
#     cost = forms.DecimalField(max_digits=10, decimal_places=2)
#     dish_type = forms.CharField(max_length=50)
#     picture = forms.ImageField()
#     class Meta:
#         model = Dish

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
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

