from django.db import models

class Products(models.Model):
	title = models.TextField()
	count = models.IntegerField()

