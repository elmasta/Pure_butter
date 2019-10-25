from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    nutrition_grades = models.CharField(max_length=1)
    ingredients = models.TextField()
    url = models.CharField(max_length=400)
    image_url = models.CharField(max_length=400)
    nutrional_url = models.CharField(max_length=400)
    user = models.ManyToManyField(User, related_name='product_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
