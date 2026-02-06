from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from .forms import UserRegistrationForm


def choice(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "main/choice.html", context)

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("home")  # redirect to homepage
    else:
        form = UserRegistrationForm()
    return render(request, "main/registration.html", {"form": form})
def authorization(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "main/authorization.html", context)

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user) 
            return redirect("home")  
    else:
        form = LoginForm()
    return render(request, "main/authorization.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")
