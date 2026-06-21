from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # DASHBOARD
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # USER MANAGEMENT
    path("users/", views.user_management, name="user_management"),
    path("users/update-role/<int:user_id>/", views.update_user_role, name="update_user_role"),
    path("users/delete/<int:user_id>/",views.delete_user,name="delete_user"),

    # REGISTER
    path("register/", views.register, name="register"),

    # LOGIN
    path("login/", views.user_login, name="login"),

    # LOGOUT
    path("logout/", views.user_logout, name="logout"),

    # PROFILE
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    path("password-change/",auth_views.PasswordChangeView.as_view(template_name="password_change.html"),name="password_change"),

    path("password-change-done/",auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),name="password_change_done"),

    # LEAD
    path("leads/", views.lead_list, name="lead_list"),
    path("leads/add/", views.add_lead, name="add_lead"),
    path("leads/edit/<int:id>/", views.edit_lead, name="edit_lead"),
    path("leads/delete/<int:id>/", views.delete_lead, name="delete_lead"),

    path("api/leads/", views.lead_api, name="lead_api"),
    path("api/leads/<int:id>/", views.lead_detail_api, name="lead_detail_api"),

    # PRODUCT
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:id>/", views.delete_product, name="delete_product"),

    path("api/products/", views.product_api, name="product_api"),
    path("api/products/<int:id>/", views.product_detail_api, name="product_detail_api"),

    # REGION
    path("regions/", views.region_list, name="region_list"),
    path("regions/add/", views.add_region, name="add_region"),
    path("regions/edit/<int:id>/", views.edit_region, name="edit_region"),
    path("regions/delete/<int:id>/", views.delete_region, name="delete_region"),

    path("api/regions/", views.region_api, name="region_api"),
    path("api/regions/<int:id>/", views.region_detail_api, name="region_detail_api"),

    # SOURCE
    path("sources/", views.source_list, name="source_list"),
    path("sources/add/", views.add_source, name="add_source"),
    path("sources/edit/<int:id>/", views.edit_source, name="edit_source"),
    path("sources/delete/<int:id>/", views.delete_source, name="delete_source"),
]