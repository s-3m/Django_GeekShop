from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Product, ProductCategory
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductCategory)
