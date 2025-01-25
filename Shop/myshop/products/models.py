from django.db import models

class Product(models.model):
    name = models.CharField(max_lenght = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name