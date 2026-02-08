from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from cook.models import Dish, Menu, Stock
from main.decorators import role_required
from .serializers import IngredientSerializer, DishSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status, generics # type: ignore
from django.db import transaction
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateMenuForm
from django.http import HttpResponseForbidden 

@role_required('cook')
class IngredientUseAPI(generics.RetrieveUpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object() 
        
        try:
            val = request.data.get('amount', 0)
            remove_amount = float(val) 
        except (ValueError, TypeError):
            return Response(
                {"error": "Введите корректное число"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if remove_amount <= 0:
            return Response(
                {"error": "Число должно быть больше 0"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if remove_amount <= instance.amount:
            instance.amount -= remove_amount
            instance.save()
            
            return Response({
                "message": f"Списано {remove_amount} единиц",
                "total": instance.amount
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"error": f"Недостаточно! Остаток: {instance.amount}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    def put(self, request, *args, **kwargs):
         return self.patch(request, *args, **kwargs)


class StockCookDishAPI(generics.RetrieveUpdateAPIView):
    queryset = Stock.objects.all()
    serializer_class = DishSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object() 
        
        try:
            val = request.data.get('amount_cooked', 0)
            add_amount = int(val) 
        except (ValueError, TypeError):
            return Response(
                {"error": "Введите корректное число"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if add_amount <= 0:
            return Response(
                {"error": "Число должно быть больше 0"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.amount_cooked += add_amount
        instance.save()
            
        return Response({"message": f"Добавлено {add_amount} единиц","total": instance.amount_cooked}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
         return self.patch(request, *args, **kwargs)




def fproducts(request):
	products = Ingredient.objects.all()
	return render(request, "cook/products.html", {"products": products})

def fdishes(request):
	dish = Dish.objects.all()
	return render(request, "cook/products.html", {"product": dish})





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
            new_menu = Menu(
                date=chosen_date,
                dish1=chosen_dish1,
                dish2=chosen_dish2,
                dish3=chosen_dish3,
                dish4=chosen_dish4,
                dish5=chosen_dish5,
                food_intake=food_intake
            )
            new_menu.save()
            messages.success(request, f"Меню на {chosen_date} ({food_intake}) успешно создано!")
            return redirect('main_page')
    else:
        form = CreateMenuForm()

    context['form'] = form
    return render(request, 'cook/create_menu.html', context)


