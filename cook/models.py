from django.db import models

class Role(models.Model):
    title = models.CharField(max_length=50, verbose_name="роль")

    def str(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО пользователя")
    login = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    def str(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    student_class = models.CharField(max_length=50, db_column='class')

    def str(self):
        return f"{self.user.name} ({self.student_class}) — {self.money} руб."

class Ingredient(models.Model):
    title = models.CharField(max_length=255)
    amount = models.FloatField(default=0)
    picture = models.ImageField(upload_to="pictures/ingredients", null=True, blank=True)

    def str(self):
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

    def str(self):
        return self.title

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

    def str(self):
        return f"Меню на {self.date} ({self.food_intake})"

class Purchases(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    deposited_money = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    date_of_meal = models.DateField()
    attendance = models.BooleanField(default=False)
    food_intake = models.CharField(max_length=50)
    type_of_purchase = models.CharField(max_length=50)
    
    def str(self):
        return f"Чек №{self.id} — {self.student.user.name}"

class Allergy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'ingredient')

class Stock(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date = models.DateField()
    expiration_date = models.DateField()
    amount_cooked = models.PositiveIntegerField()
    amount_sold = models.PositiveIntegerField()
    
    def str(self):
        return f"{self.dish.title} от {self.date}"
class OrderStatus(models.Model):
    description = models.CharField(max_length=255)
    
    def str(self):
        return self.description

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)

    def str(self):

        return f"Заказ: {self.ingredient.title} ({self.status})"

class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    comment = models.TextField()
    mark = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)
    
    def str(self):
        return f"Отзыв от {self.student.user.name}"