from rest_framework import serializers
from .models import Stock, Dish, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'title', 'amount']

class DishSerializer(serializers.ModelSerializer):

    dish_name = serializers.CharField(source='dish.title', read_only=True)
    class Meta:
        model = Stock
        fields = ['id', 'amount_cooked','dish_name' ]