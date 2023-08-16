from django.db import models
from .customer import Customer
from .book import Book

class CustomerBook(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
