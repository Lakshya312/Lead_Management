from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('regions/', views.region_list, name='region_list'),
    path('regions/add/', views.add_region, name='add_region'),
    path('regions/edit/<int:id>/', views.edit_region, name='edit_region'),
    path('regions/delete/<int:id>/', views.delete_region, name='delete_region'),

]