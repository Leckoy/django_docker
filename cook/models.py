from django.db import models

class products(models.Model):
	title = models.TextField()
	count = models.IntegerField()
	picture = models.ImageField(upload_to="pictures/products")


class dishes(models.Model):
	title = models.TextField()
	count = models.IntegerField()
	picture = models.ImageField(upload_to="picture/dishes")
