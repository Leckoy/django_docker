from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from cook.models import Dish, Menu, Stock
from main.decorators import role_required
# from cook.models import dishes
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore
from django.db import transaction
from .models import Student, Purchases, Allergy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentOrderForm

@role_required('Student')
def index(request: HttpRequest) -> HttpResponse:
    context = {"title": "Главная страница"}
    return render(request, "student/index.html", context)

def menu(request: HttpRequest) -> HttpResponse:
    context = {"dishes" : Dish.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:
    return render(request, "student/allergy.html")

def top_up(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/top_up.html", context)

#def pay_onetime(request: HttpRequest) -> HttpResponse:
    #context = {}
    # return render(request, "student/pay_onetime.html", context)

def season_ticket(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/season_ticket.html", context)

def comment(request: HttpRequest, dish_id) -> HttpResponse:
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, "student/comment.html", {"dish": dish})





def pay_onetime(request: HttpRequest) -> HttpResponse:
    context = {}

    student = request.user.student_profile
    
    if request.method == 'POST':
        form = StudentOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            chosen_date = form.cleaned_data.get('date_of_meal')
            menu_for_day = Menu.objects.filter(date=chosen_date).first()
            order.menu_id = menu_for_day.id
            price = menu_for_day.dish1.cost + menu_for_day.dish2.cost + menu_for_day.dish3.cost + menu_for_day.dish4.cost +menu_for_day.dish5.cost


            if student.money < price:
                messages.error(request, "У вас недостаточно денег на балансе!")
            else:
                with transaction.atomic():
                    student.money -= price
                    student.save()
                    
                    order.student = student
                    order.deposited_money = price
                    order.type_of_purchase = "Баланс"

                    order.save()

                    
                    messages.success(request, f"Заказ на {order.food_intake} успешно оформлен!")
                    return redirect('main_page') 
    else:
        form = StudentOrderForm()

    return render(request, 'student/pay_onetime.html', {
        'form': form,
        'balance': student.money
    })





























