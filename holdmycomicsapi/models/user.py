from django.db import models

class User(models.Model):
    """Model that represents a user"""
    uid = models.CharField(max_length=50)
    user_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
