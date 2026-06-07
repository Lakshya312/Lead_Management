from django.urls import path
from . import views

urlpatterns = [
    # 1. Main display page
    path('products/', views.product_list, name='product_list'),
    
    # 2. Explicit action URLs
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:productid>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:productid>/', views.delete_product, name='delete_product'),
]