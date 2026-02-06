from django import forms
from .models import User, Role
from django.contrib.auth import authenticate

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
        user.set_password(self.cleaned_data["password1"])  # hash password
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if login and password:
            user = authenticate(login=login, password=password)
            if user is None:
                raise forms.ValidationError("Invalid login or password")
            cleaned_data["user"] = user
        return cleaned_data