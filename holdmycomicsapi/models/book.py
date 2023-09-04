from django.db import models

class Book(models.Model):
    """Model that represents a book"""
    image_url = models.CharField(max_length=200)
    publisher = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
