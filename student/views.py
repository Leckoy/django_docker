from django.db.models import Sum

from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from cook.models import Dish, Menu,Review, Stock, Composition
from main.decorators import role_required
from datetime import timedelta
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore
from django.db import transaction, IntegrityError

from django.http import HttpRequest, HttpResponse
from cook.models import Dish, Menu, Review, Stock, Ingredient
from main.decorators import role_required

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore

from django.db import transaction

from .models import Student, Purchases, Allergy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentOrderForm, AddAllergyForm, FeedBackForm, TopUpForm

from .forms import StudentOrderForm, FeedBackForm
from decimal import Decimal

def dish_or_0(dish: Dish):
    return dish.cost if dish else Decimal('0')




def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    context = {"title": "Главная страница"}
    return render(request, "student/index.html", context)

def menu(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    context = {"dishes" : Dish.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
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
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")


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
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    try:
        student = request.user.student_profile
        allergy = get_object_or_404(Allergy, id=allergy_id, student=student)
        allergy.delete()
    except:
        pass
    return redirect("allergy_page")

def top_up(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    try:
        student = request.user.student_profile
    except:
        return redirect('login')

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                summa = form.cleaned_data['summa']
                if not isinstance(summa, Decimal):
                    summa = Decimal(str(summa))
                    
                student.money += summa
                student.save()

                return redirect('main_page') 
    else:
        form = TopUpForm()

    return render(request, "student/top_up.html", {"form": form})

def season_ticket(request: HttpRequest) -> HttpResponse:
    
    context = {}
    return render(request, "student/season_ticket.html", context)

def comment(request: HttpRequest, dish_id) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, "student/comment.html", {"dish": dish})





def pay_onetime(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    
    student = request.user.student_profile
    if request.method == 'POST':
        form = StudentOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            chosen_date = form.cleaned_data.get('date_of_meal')
            chosen_food_intake = form.cleaned_data.get('food_intake')

            menu_for_day = Menu.objects.filter(date=chosen_date, food_intake=chosen_food_intake).first()
            if menu_for_day is None:
                messages.error(request, "Меню на этот день не создано")
                return render(request, 'student/pay_onetime.html', {'form': form})

            order.menu_id = menu_for_day.id
            price = dish_or_0(menu_for_day.dish1) + dish_or_0(menu_for_day.dish2) + dish_or_0(menu_for_day.dish3) + dish_or_0(menu_for_day.dish4) + dish_or_0(menu_for_day.dish5)

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
        'balance': student.money,
    })


def Menu_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

    student = request.user.student_profile
    now = timezone.now().date()

    allergies_object = Allergy.objects.filter(student=student)
    allergies_ingredients = [allergy.ingredient for allergy in allergies_object]

    m1_breakfast = Menu.objects.filter(date=now - timedelta(days=1), food_intake="Завтрак").first()
    m1_lunch = Menu.objects.filter(date=now - timedelta(days=1),food_intake="Обед").first()

    m2_breakfast = Menu.objects.filter(date=now, food_intake="Завтрак").first()
    m2_lunch = Menu.objects.filter(date=now,food_intake="Обед").first()

    m3_breakfast = Menu.objects.filter(date=now + timedelta(days=1), food_intake="Завтрак").first()
    m3_lunch = Menu.objects.filter(date=now + timedelta(days=1),food_intake="Обед").first()

    m4_breakfast = Menu.objects.filter(date=now + timedelta(days=2), food_intake="Завтрак").first()
    m4_lunch = Menu.objects.filter(date=now + timedelta(days=2),food_intake="Обед").first()
    
    m5_breakfast = Menu.objects.filter(date=now + timedelta(days=3), food_intake="Завтрак").first()
    m5_lunch = Menu.objects.filter(date=now + timedelta(days=3),food_intake="Обед").first()

    m6_breakfast = Menu.objects.filter(date=now + timedelta(days=4), food_intake="Завтрак").first()
    m6_lunch = Menu.objects.filter(date=now + timedelta(days=4),food_intake="Обед").first()

    m7_breakfast = Menu.objects.filter(date=now + timedelta(days=5), food_intake="Завтрак").first()
    m7_lunch = Menu.objects.filter(date=now + timedelta(days=5),food_intake="Обед").first()

    price1_breakfast = m1_breakfast.get_total_cost() if m1_breakfast else 0
    price1_lunch = m1_lunch.get_total_cost() if m1_lunch else 0

    price2_breakfast = m2_breakfast.get_total_cost() if m2_breakfast else 0
    price2_lunch = m2_lunch.get_total_cost() if m2_lunch else 0

    price3_breakfast = m3_breakfast.get_total_cost() if m3_breakfast else 0
    price3_lunch = m3_lunch.get_total_cost() if m3_lunch else 0

    price4_breakfast = m4_breakfast.get_total_cost() if m4_breakfast else 0
    price4_lunch = m4_lunch.get_total_cost() if m4_lunch else 0

    price5_breakfast = m5_breakfast.get_total_cost() if m5_breakfast else 0
    price5_lunch = m5_lunch.get_total_cost() if m5_lunch else 0

    price6_breakfast = m6_breakfast.get_total_cost() if m6_breakfast else 0
    price6_lunch = m6_lunch.get_total_cost() if m6_lunch else 0

    price7_breakfast = m7_breakfast.get_total_cost() if m7_breakfast else 0
    price7_lunch = m7_lunch.get_total_cost() if m7_lunch else 0

    days_data = [
        {
            'title': 'Вчера',
            'meals': [
                    {'name': 'Завтрак', 'menu':m1_breakfast, 'price': price1_breakfast},
                    {'name': 'Обед', 'menu': m1_lunch, 'price': price1_lunch},
                ],
        },

        {
            'title': 'Сегодня',
            'meals': [
                {'name': 'Завтрак', 'menu':m2_breakfast, 'price': price2_breakfast},
                {'name': 'Обед', 'menu': m2_lunch, 'price': price2_lunch},
            ],
        },

        {
            'title': 'Завтра',
            'meals': [
                {'name': 'Завтрак', 'menu':m3_breakfast, 'price': price3_breakfast},
                {'name': 'Обед', 'menu': m3_lunch, 'price': price3_lunch},
            ],
        },

        {
            'title': 'Послезавтра',
            'meals': [
                {'name': 'Завтрак', 'menu':m4_breakfast, 'price': price4_breakfast},
                {'name': 'Обед', 'menu': m4_lunch, 'price': price4_lunch},
            ],
        },

        {
            'title': 'Через 3 дня',
            'meals': [
                {'name': 'Завтрак', 'menu':m5_breakfast, 'price': price5_breakfast},
                {'name': 'Обед', 'menu': m5_lunch, 'price': price5_lunch},
            ],
        },

        {
            'title': 'Через 4 дня',
            'meals': [
                {'name': 'Завтрак', 'menu':m6_breakfast, 'price': price6_breakfast},
                {'name': 'Обед', 'menu': m6_lunch, 'price': price6_lunch},
            ],
        },

        {
            'title': 'Через 3 дня',
            'meals': [
                {'name': 'Завтрак', 'menu':m7_breakfast, 'price': price7_breakfast},
                {'name': 'Обед', 'menu': m7_lunch, 'price': price7_lunch},
            ],
        }
    ]
                

    return render(request, 'student/menu.html', {
        'balance': student.money,
        'days': days_data,
        "allergies": allergies_ingredients,
    })

def FeedBack(request: HttpRequest,dish_id: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 2: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь учеником.")

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
            return redirect('/student/menu/') 
        else:
            messages.error(request, "Ошибка: проверьте данные формы.")
    else:
        form = FeedBackForm()
    return render(request, 'student/comment.html', {
            'form': form,
            'dish': dish
        })























