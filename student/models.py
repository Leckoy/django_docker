from django.db import models

class Student(models.Model):
    user = models.OneToOneField('main.User', on_delete=models.CASCADE, related_name="student_profile")
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    student_class = models.CharField(max_length=50, db_column='class')

    def __str__(self):
        return f"{self.user.name} ({self.student_class}) — {self.money} руб."

class Purchases(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    menu = models.ForeignKey('cook.Menu', on_delete=models.CASCADE)
    deposited_money = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True,null=True)
    date_of_meal = models.DateField()
    attendance = models.BooleanField(default=False)
    food_intake = models.CharField(max_length=50)
    type_of_purchase = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Чек №{self.id} — {self.student.user.name}"


class Allergy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('cook.Ingredient', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'ingredient')