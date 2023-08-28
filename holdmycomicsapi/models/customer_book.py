from django.db import models
from .customer import Customer
from .book import Book

class CustomerBook(models.Model):
    """Model that represents a book ordered by a customer"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

# Foreign Key is a field in a model that takes in other models

# seeded data the data is put in the database
# fixture by itself is not seeded data
# a fixture is a JSON file that stores data to seed your database, also stores model information
# you use fixtures to seed data but fixtures themselves are NOT seeded data
# will be asked why you use Postman instead of seeded data
# you can use seeded data to test database without going through front end, make sure API calls work
# initial set of data to populate a database
