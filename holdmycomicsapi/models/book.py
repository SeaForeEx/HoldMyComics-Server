from django.db import models
from .user import User

class Book(models.Model):
    """Model that represents a user"""
    store_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    publisher = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
