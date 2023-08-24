from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255) 
    price = models.IntegerField()
    categoria=models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.nombre} -> {self.price}'