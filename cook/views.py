from django.db.models import Sum
from django.http import HttpRequest,HttpResponseForbidden, HttpResponse
from cook.models import Dish, Menu, Stock, Ingredient
from main.decorators import role_required
from .serializers import IngredientSerializer, DishSerializer
from decimal import Decimal
from django.db import transaction
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateMenuForm, IngredientOrdeForm, IngredientUseForm, DishAddForm
from datetime import timedelta
from django.utils import timezone






def fproducts(request):
	products = Ingredient.objects.all()
	return render(request, "cook/products.html", {"products": products})

def fdishes(request):
	dish = Dish.objects.all()
	return render(request, "cook/products.html", {"product": dish})


def index(request):
    return render(request, "cook/index.html", {"title": "Home page"})


def CreateMenu(request: HttpRequest) -> HttpResponse:
    context = {}

    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 3: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")


    if request.method == 'POST':
        form = CreateMenuForm(request.POST)
        if form.is_valid():
            chosen_date = form.cleaned_data.get('date')
            chosen_dish1 = form.cleaned_data.get('dish1')
            chosen_dish2 = form.cleaned_data.get('dish2')
            chosen_dish3 = form.cleaned_data.get('dish3')
            chosen_dish4 = form.cleaned_data.get('dish4')
            chosen_dish5 = form.cleaned_data.get('dish5')
            food_intake = form.cleaned_data.get('food_intake')

            new_menu, created = Menu.objects.update_or_create(
                date=chosen_date,
                food_intake=food_intake,
                defaults={
                    'dish1': chosen_dish1,
                    'dish2': chosen_dish2,
                    'dish3': chosen_dish3,
                    'dish4': chosen_dish4,
                    'dish5': chosen_dish5,
                }
            )
            if created:
                messages.success(request, f"Меню на {chosen_date} ({food_intake}) успешно создано!")
            else:
                messages.success(request, f"Меню на {chosen_date} ({food_intake}) успешно обновлено (старое затерто)!")
                
            return redirect('create_menu')
    else:
        form = CreateMenuForm()

    context['form'] = form
    return render(request, 'cook/create_menu.html', context)


def IngredientUse(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 3: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")


    if request.method == 'POST':
        form = IngredientUseForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data.get('amount')
            ingr = form.cleaned_data.get('title')

            if ingr.amount < count:
                messages.error(request, "У вас недостаточно ингредиентов")
            else:
                ingr.amount -= count
                ingr.save()

                return redirect("ingredient") 
        else:
            messages.error(request, "Ошибка: выберите ингредиент из списка.")
    else:
        form = IngredientUseForm()
    all_ingredients = Ingredient.objects.all()
    return render(request, 'cook/ingredient.html', {
            'form': form,
            'all_ingredients': all_ingredients
        })


def IngredientOrder(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 3: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")


    if request.method == 'POST':
        form = IngredientOrdeForm(request.POST)
        if form.is_valid():
            new_order = Order()
            count = form.cleaned_data.get('amount')
            ingr = form.cleaned_data.get('title')
            new_order.ingredient = ingr
            new_order.amount = count
            new_order.cost = ingr.cost * Decimal(str(count))
            new_order.status = 0
            new_order.save()
            return redirect('/cook/order/') 
        else:
            messages.error(request, "Ошибка: проверьте данные формы.")
    else:
        form = IngredientOrdeForm()
    all_ingredients = Ingredient.objects.all()
    return render(request, 'cook/order.html', {
            'form': form,
            'all_ingredients': all_ingredients
        })




def DishAdd(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 3: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")


    if request.method == 'POST':
        form = DishAddForm(request.POST)
        if form.is_valid():
            weigh = form.cleaned_data.get('weigh')
            dishh = form.cleaned_data.get('title')

            if 0 > weigh:
                messages.error(request, "Введите корректное число")
            else:
                dishh.weight += weigh
                dishh.save()
                return redirect('dish') 
        else:
            messages.error(request, "Ошибка: выберите блюдо из списка.")
    else:
        form = DishAddForm()
    all_ingredients = Dish.objects.all()
    return render(request, 'cook/dish.html', {
            'form': form,
            'all_ingredients': all_ingredients
        })

def Menu_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_role_id = request.user.role.id if request.user.role else None
    if user_role_id != 3: 
        return HttpResponseForbidden("Доступ запрещен: вы не являетесь поваром.")
    
    now = timezone.now().date()

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
            'title': 'Через 5 дней',
            'meals': [
                {'name': 'Завтрак', 'menu':m7_breakfast, 'price': price7_breakfast},
                {'name': 'Обед', 'menu': m7_lunch, 'price': price7_lunch},
            ],
        }
    ]
                

    return render(request, 'cook/menu.html', {
        'days': days_data,
    })