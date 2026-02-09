from django.db.models import Sum
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from cook.models import Dish, Menu,Review, Stock
from main.decorators import role_required
from datetime import timedelta
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore
from django.db import transaction, IntegrityError
from .models import Student, Purchases, Allergy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import StudentOrderForm, AddAllergyForm, FeedBackForm

@role_required('Student')
def index(request: HttpRequest) -> HttpResponse:
    context = {"title": "Главная страница"}
    return render(request, "student/index.html", context)

def menu(request: HttpRequest) -> HttpResponse:
    context = {"dishes" : Dish.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:

    student = request.user.student_profile
    if request.method == "POST":

        form = AddAllergyForm(request.POST)

        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.student = student
            try:
                allergy.save()
                return redirect('allergy_page')
            except IntegrityError:
                form.add_error(None, "Эта аллергия уже существует")
    
    else:
        form = AddAllergyForm()

    return render(request, "student/allergy.html", {
        "form":form,
        "allergies": Allergy.objects.filter(student=student)
        })
def FeedBack(request: HttpRequest,dish_id: int) -> HttpResponse:
    context = {}

    student = request.user.student_profile
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            new_komment = Review()

            mark = form.cleaned_data.get('mark')
            comment = form.cleaned_data.get('comment')
            new_komment.comment = comment
            new_komment.mark = mark
            new_komment.date = timezone.now()
            new_komment.dish = dish
            new_komment.student = student
            new_komment.save()
            return redirect('menu_page') 
        else:
            messages.error(request, "Ошибка: проверьте данные формы.")
    else:
        form = FeedBackForm()
    return render(request, 'student/comment.html', {
            'form': form,
            'dish': dish
        })



def allergy_delete(request: HttpRequest, allergy_id)-> HttpResponse:
    try:
        student = request.user.student_profile
        allergy = get_object_or_404(Allergy, id=allergy_id, student=student)
        allergy.delete()
    except:
        pass
    return redirect("allergy_page")

def top_up(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/top_up.html", context)

def season_ticket(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/season_ticket.html", context)

def comment(request: HttpRequest, dish_id) -> HttpResponse:
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, "student/comment.html", {"dish": dish})





def pay_onetime(request: HttpRequest) -> HttpResponse:

    student = request.user.student_profile
    
    if request.method == 'POST':
        form = StudentOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            chosen_date = form.cleaned_data.get('date_of_meal')
            menu_for_day = Menu.objects.filter(date=chosen_date).first()
            if menu_for_day is None:
                messages.error(request, "Меню на этот день не создано")
                return render(request, 'student/pay_onetime.html', {'form': form})

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


def Menu_view(request):

    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")
    student = request.user.student_profile
    now = timezone.now().date()
    m1 = Menu.objects.filter(date=now - timedelta(days=1)).first()
    print(m1)
    print(now)
    m2 = Menu.objects.filter(date=now).first()
    m3 = Menu.objects.filter(date=now + timedelta(days=1)).first()
    m4 = Menu.objects.filter(date=now + timedelta(days=2)).first()
    m5 = Menu.objects.filter(date=now + timedelta(days=3)).first()
    m6 = Menu.objects.filter(date=now + timedelta(days=4)).first()
    m7 = Menu.objects.filter(date=now + timedelta(days=5)).first()

    price1 = m1.get_total_cost() if m1 else 0
    price2 = m2.get_total_cost() if m2 else 0
    price3 = m3.get_total_cost() if m3 else 0
    price4 = m4.get_total_cost() if m4 else 0
    price5 = m5.get_total_cost() if m5 else 0
    price6 = m6.get_total_cost() if m6 else 0
    price7 = m7.get_total_cost() if m7 else 0

    return render(request, 'student/menu.html', {
        'balance': student.money,
        'price1': price1, 
        'price2': price2, 
        'price3': price3,
        'price4': price4, 
        'price5': price5, 
        'price6': price6, 
        'price7': price7,
        'm1': m1, 
        'm2': m2, 
        'm3': m3, 
        'm4': m4, 
        'm5': m5, 
        'm6': m6, 
        'm7': m7,
    })
























