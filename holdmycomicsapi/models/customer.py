from django.db import models
from .user import User

class Customer(models.Model):
    """Model that represents a customer"""
    store_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default='')
