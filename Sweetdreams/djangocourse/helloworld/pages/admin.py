from django.contrib import admin
from .models import Category, Product, Organization, User, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Organization)
admin.site.register(User)
admin.site.register(Order)
