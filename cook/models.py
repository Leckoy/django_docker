from django.db import models
from main.models import User


class Ingredient(models.Model):
    title = models.CharField(max_length=255)
    amount = models.FloatField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to="pictures/ingredients", null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.amount} г"

class Dish(models.Model):
    title = models.CharField(max_length=255)
    weight = models.FloatField(verbose_name="Вес (г)")
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="pictures/dishes", null=True, blank=True)
    
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='Composition', 
        related_name="dishes"
    )

    def __str__(self):
        return self.title
    
    def get_ingredients(self):
        return [ingr for ingr in self.ingredients.all()]

class Composition(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name="Вес ингредиента в блюде")

class Menu(models.Model):
    food_intake = models.CharField(max_length=50, verbose_name="Прием пищи")
    date = models.DateField()
    
    dish1 = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="menu_pos1")
    dish2 = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="menu_pos2")
    dish3 = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="menu_pos3")
    dish4 = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="menu_pos4")
    dish5 = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, related_name="menu_pos5")

    def __str__(self):
        return f"Меню на {self.date} ({self.food_intake})"
        return self.name
    
    def get_total_cost(self):
        dishes = [self.dish1, self.dish2, self.dish3, self.dish4, self.dish5]
        return sum(dish.cost for dish in dishes if dish)
    
    def get_dishes(self):
        return [self.dish1, self.dish2, self.dish3, self.dish4, self.dish5]



class Stock(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True,null=True)
    expiration_date = models.DateField(auto_now_add=True,null=True)
    amount_cooked = models.PositiveIntegerField()
    amount_sold = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.dish.title} от {self.date}"
    
class OrderStatus(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description

class Order(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.FloatField()
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):

        return f"Заказ: {self.ingredient.title} ({self.status})"

class Review(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    mark = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Отзыв от {self.student.user.name}"