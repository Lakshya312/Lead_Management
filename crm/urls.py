from django.urls import path
from .views import *

urlpatterns = [
    # for products

    path('products/', Product_view.product_list, name='product_list'),
    path('products/add/', Product_view.add_product, name='add_product'),
    path('products/edit/<int:productid>/', Product_view.edit_product, name='edit_product'),
    path('products/delete/<int:productid>/', Product_view.delete_product, name='delete_product'),

    # for regions
    path('regions/', Region_view.region_list, name='region_list'),
    path('regions/add/', Region_view.add_region, name='add_region'),
    path('regions/edit/<int:regionid>/', Region_view.edit_region, name='edit_region'),
    path('regions/delete/<int:regionid>/', Region_view.delete_region, name='delete_region'),

    path('leads/', Lead_view.lead_list, name='lead_list'),
    path('leads/add/', Lead_view.add_lead, name='add_lead'),
    path('leads/edit/<int:leadid>/', Lead_view.edit_lead, name='edit_lead'),
    path('leads/delete/<int:leadid>/', Lead_view.delete_lead, name='delete_lead'),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # API SECTION
    path('api/products/',product_api,name='product_api'),
    path('api/products/<int:productid>/', update_product_api),
    path('api/products/<int:productid>/delete/', delete_product_api),

    path('api/leads/', lead_api, name='lead_api'),
    path('api/leads/<int:leadid>/', update_lead_api),
    path('api/leads/<int:leadid>/delete/', delete_lead_api),

    path('api/regions/', region_api, name='region_api'),
    path('api/regions/<int:regionid>/', update_region_api),
    path('api/regions/<int:regionid>/delete/', delete_region_api),

    # VALIDATIONS
    # FOR LEAD
    path('check-personname/',check_personname,name='check_personname'),
    path('check-contactno/',check_contactno,name='check_contactno'),
    path('check-email/',check_email,name='check_email'),

    # FOR PRODUCT
    path('check-productname/',check_productname,name='check_productname'),

    # FOR REGION
    path('check-regionname/',check_regionname,name='check_regionname'),


]