from django.shortcuts import render 
from django.http import HttpResponse 
from .models import Ingredient,Dish
from rest_framework import generics
from .models import Ingredient, Stock
from .serializers import IngredientSerializer, DishSerializer
from rest_framework.response import Response
from rest_framework import status             
from django.utils import timezone
from main.decorators import role_required

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





def index(request):
	return render(request, "cook/index.html")
def copy(request):
	return render(request, "cook/copy.html")
# Create your views here.
