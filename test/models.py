from django.db import models

class products(models.Model):
	title = models.TextField()
	count = models.IntegerField()

