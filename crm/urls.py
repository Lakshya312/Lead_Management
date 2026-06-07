from django.urls import path
from .views import *

urlpatterns = [
    # for products

    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/edit/<int:productid>/', edit_product, name='edit_product'),
    path('products/delete/<int:productid>/', delete_product, name='delete_product'),

    # for regions
    path('regions/', region_list, name='region_list'),
    path('regions/add/', add_region, name='add_region'),
    path('regions/edit/<int:regionid>/', edit_region, name='edit_region'),
    path('regions/delete/<int:regionid>/', delete_region, name='delete_region'),
]