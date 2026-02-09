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
            from cook.models import Menu
           
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
    context = {}

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
    context = {}

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
    context = {}

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