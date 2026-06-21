"""
URL configuration for the leads app.

Uses DRF's DefaultRouter to auto-generate RESTful URL patterns for all API endpoints.
All API endpoints are prefixed with 'api/'.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'leads'

# DRF Router — auto-generates list and detail URL patterns for each ViewSet
router = DefaultRouter()
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'categories', views.ProductCategoryViewSet, basename='category')
router.register(r'lead-sources', views.LeadSourceViewSet, basename='lead-source')
router.register(r'lead-statuses', views.LeadStatusViewSet, basename='lead-status')
router.register(r'territories', views.TerritoryViewSet, basename='territory')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'follow-ups', views.LeadFollowUpViewSet, basename='follow-up')

urlpatterns = [
    # API endpoints (browsable API root at /api/)
    path('api/', include(router.urls)),
    
    # Frontend endpoints
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    path('regions/', views.RegionListView.as_view(), name='region_list'),
    path('regions/add/', views.RegionCreateView.as_view(), name='region_add'),
    path('regions/<int:pk>/edit/', views.RegionUpdateView.as_view(), name='region_edit'),
    path('regions/<int:pk>/delete/', views.RegionDeleteView.as_view(), name='region_delete'),
    
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    path('leads/', views.LeadListView.as_view(), name='lead_list'),
    path('leads/add/', views.LeadCreateView.as_view(), name='lead_add'),
    path('leads/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='lead_edit'),
    path('leads/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead_delete'),
]
