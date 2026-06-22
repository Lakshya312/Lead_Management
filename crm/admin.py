from django.contrib import admin
from .models import Product, ProductCategory, Region

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Region)