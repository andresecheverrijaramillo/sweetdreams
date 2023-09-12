from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255) 
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) 
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default='1')
    image = models.ImageField(upload_to='uploads/products', null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=30, default='')
    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.product
