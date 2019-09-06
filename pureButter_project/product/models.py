from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

class User(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    nutrition_grades = models.CharField(max_length=1)
    ingredients = models.TextField()
    url = models.CharField(max_length=400)
    user = models.ManyToManyField(User, related_name='product_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
