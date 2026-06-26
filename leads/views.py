"""
API views for the leads app.

Provides full CRUD (Create, Read, Update, Delete) endpoints for all models
using Django REST Framework ModelViewSets with filtering, searching, and ordering.

Exception Handling Strategy (views.py):
  - ProtectedError on DELETE  → HTTP 409 Conflict (all ViewSets + UI Delete views)
  - General Exception on DELETE → HTTP 500 with error logged (safety net)
  - DB errors in DashboardView → HTTP 500 with flash message + log entry
  - All exceptions are recorded to logs/errors.log via the 'leads' logger
"""
import logging

from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Region, ProductCategory, LeadSource, LeadStatus,
    Territory, Product, Lead, LeadFollowUp,
)
from .serializers import (
    RegionSerializer, ProductCategorySerializer,
    LeadSourceSerializer, LeadStatusSerializer,
    TerritorySerializer, ProductSerializer,
    LeadSerializer, LeadFollowUpSerializer,
)

# ---------------------------------------------------------------------------
# Module-level logger — all messages flow to logs/errors.log & logs/general.log
# ---------------------------------------------------------------------------
logger = logging.getLogger('leads')


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms as django_forms
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages as contrib_messages


class CRMUserCreationForm(UserCreationForm):
    """
    Extended user registration form that collects first name, last name, and email.
    Inherits all password validation from Django's built-in UserCreationForm.
    """
    first_name = django_forms.CharField(
        max_length=30, required=False,
        widget=django_forms.TextInput(attrs={'placeholder': 'John'}),
    )
    last_name = django_forms.CharField(
        max_length=150, required=False,
        widget=django_forms.TextInput(attrs={'placeholder': 'Doe'}),
    )
    email = django_forms.EmailField(
        required=False,
        widget=django_forms.EmailInput(attrs={'placeholder': 'john@company.com'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name  = self.cleaned_data.get('last_name', '')
        user.email      = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


class LoginView(View):
    """
    Handles GET (render login form) and POST (authenticate & login).
    Redirects authenticated users directly to the dashboard.
    """
    template_name = 'registration/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('leads:dashboard')
        form = AuthenticationForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info("LoginView: User '%s' logged in successfully.", user.username)
            contrib_messages.success(request, f"Welcome back, {user.get_full_name() or user.username}! 👋")
            next_url = request.GET.get('next') or 'leads:dashboard'
            return redirect(next_url)
        else:
            logger.warning(
                "LoginView: Failed login attempt. Errors: %s",
                form.errors,
            )
            contrib_messages.error(request, "Invalid username or password. Please try again.")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    Handles POST-only logout (CSRF protected) and redirects to login page.
    """
    def post(self, request):
        username = request.user.username if request.user.is_authenticated else 'Unknown'
        logout(request)
        logger.info("LogoutView: User '%s' logged out.", username)
        contrib_messages.success(request, "You have been signed out successfully.")
        return redirect('leads:login')

    def get(self, request):
        # Redirect GET requests to login; logout should be POST only
        return redirect('leads:login')


class RegisterView(View):
    """
    Handles GET (render registration form) and POST (create user account).
    Uses extended CRMUserCreationForm with first name, last name, email.
    """
    template_name = 'registration/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('leads:dashboard')
        form = CRMUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CRMUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(
                "RegisterView: New user '%s' (%s %s) registered and logged in.",
                user.username, user.first_name, user.last_name,
            )
            contrib_messages.success(
                request,
                f"Account created successfully! Welcome, {user.get_full_name() or user.username}! 🎉"
            )
            return redirect('leads:dashboard')
        else:
            logger.warning(
                "RegisterView: Registration failed for username='%s'. Errors: %s",
                request.POST.get('username', ''), form.errors,
            )
        return render(request, self.template_name, {'form': form})


# ==============================================================================
# API VIEWSETS (Django REST Framework)
# ==============================================================================

class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Region master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Search: regionname
    Ordering: regionid, regionname
    Delete is blocked if any Territory or Lead references this Region.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    search_fields = ['regionname']
    ordering_fields = ['regionid', 'regionname']
    ordering = ['regionid']

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            # 🔴 LOG: Referenced FK constraint violation
            logger.warning(
                "RegionViewSet.destroy: ProtectedError — Region pk=%s is "
                "referenced by Territory or Lead. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Region because it is referenced by existing Territories or Leads. Remove those records first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            # 🔴 LOG: Unexpected error safety net
            logger.error(
                "RegionViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Region. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Product Category master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Search: categoryname
    Ordering: categoryid, categoryname
    Delete is blocked if any Product references this Category.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    search_fields = ['categoryname']
    ordering_fields = ['categoryid', 'categoryname']
    ordering = ['categoryid']

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "ProductCategoryViewSet.destroy: ProtectedError — Category pk=%s "
                "is referenced by Products. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Product Category because it is referenced by existing Products. Remove those products first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "ProductCategoryViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Category. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LeadSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lead Source master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Search: leadsourcename
    Ordering: leadsourceid, leadsourcename
    Delete is blocked if any Lead references this Lead Source.
    """
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    search_fields = ['leadsourcename']
    ordering_fields = ['leadsourceid', 'leadsourcename']
    ordering = ['leadsourceid']

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "LeadSourceViewSet.destroy: ProtectedError — LeadSource pk=%s "
                "is referenced by Leads. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Lead Source because it is referenced by existing Leads. Remove those leads first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "LeadSourceViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Lead Source. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LeadStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lead Status master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Search: statusname
    Ordering: statusid, statusname
    Delete is blocked if any Lead or LeadFollowUp references this Status.
    """
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    search_fields = ['statusname']
    ordering_fields = ['statusid', 'statusname']
    ordering = ['statusid']

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "LeadStatusViewSet.destroy: ProtectedError — LeadStatus pk=%s "
                "is referenced by Leads or FollowUps. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Lead Status because it is referenced by existing Leads or Follow-Ups. Remove those records first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "LeadStatusViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Lead Status. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TerritoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Territory master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Filter: regionid
    Search: territoryname
    Ordering: territoryid, territoryname
    Delete is blocked if any Lead references this Territory.
    """
    queryset = Territory.objects.select_related('regionid').all()
    serializer_class = TerritorySerializer
    filterset_fields = ['regionid']
    search_fields = ['territoryname']
    ordering_fields = ['territoryid', 'territoryname']
    ordering = ['territoryid']

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "TerritoryViewSet.destroy: ProtectedError — Territory pk=%s "
                "is referenced by Leads. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Territory because it is referenced by existing Leads. Remove those leads first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "TerritoryViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Territory. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Product master data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Filter: categoryid, is_active
    Search: productname
    Ordering: productid, productname
    Delete is blocked if any Lead references this Product.

    Custom JSON responses:
      - GET  /api/products/  → { "success": true, "count": N, "data": [...] }
      - POST /api/products/  → { "message": "Product Added Successfully" }
    """
    queryset = Product.objects.select_related('categoryid').all()
    serializer_class = ProductSerializer
    filterset_fields = ['categoryid', 'is_active']
    search_fields = ['productname']
    ordering_fields = ['productid', 'productname']
    ordering = ['productid']

    def list(self, request, *args, **kwargs):
        """
        Override list to wrap response in:
        { "success": true, "count": <total>, "data": [...] }
        """
        # ✅ NEW — wrap list in try/except to guard against unexpected filter/DB errors
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            logger.info("ProductViewSet.list: Returned %d products.", queryset.count())
            return Response({
                "success": True,
                "count": queryset.count(),
                "data": serializer.data,
            })
        except Exception as exc:
            logger.error(
                "ProductViewSet.list: Unexpected error — %s", exc, exc_info=True,
            )
            return Response(
                {"error": "Failed to retrieve products. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        """
        Override create to return:
        { "message": "Product Added Successfully" }
        """
        # ✅ NEW — guard serializer validation + DB write
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(
                "ProductViewSet.create: Product '%s' created successfully.",
                request.data.get('productname', 'unknown'),
            )
            return Response(
                {"message": "Product Added Successfully"},
                status=drf_status.HTTP_201_CREATED,
            )
        except Exception as exc:
            logger.error(
                "ProductViewSet.create: Unexpected error — %s", exc, exc_info=True,
            )
            raise  # Re-raise so DRF handles ValidationError → HTTP 400 normally

    # ✅ EXISTING — ProtectedError on delete
    def destroy(self, request, *args, **kwargs):
        """Block deletion if any Lead references this Product."""
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "ProductViewSet.destroy: ProtectedError — Product pk=%s "
                "is referenced by Leads. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Product because it is referenced by existing Leads. Remove those leads first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "ProductViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Product. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LeadViewSet(viewsets.ModelViewSet):
    """
    API endpoint for core Lead data.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Filter: regionid, statusid, leadsourceid, productid, territoryid, gender
    Search: personname, companyname, email, contactno, city
    Ordering: leadid, personname, companyname, lead_gen_date
    """
    queryset = Lead.objects.select_related(
        'territoryid', 'regionid', 'productid', 'statusid', 'leadsourceid'
    ).filter(is_deleted=False)
    serializer_class = LeadSerializer
    filterset_fields = [
        'regionid', 'statusid', 'leadsourceid',
        'productid', 'territoryid', 'gender',
    ]
    search_fields = ['personname', 'companyname', 'email', 'contactno', 'city']
    ordering_fields = ['leadid', 'personname', 'companyname', 'lead_gen_date']
    ordering = ['leadid']

    # ✅ NEW — Soft Delete for API
    def destroy(self, request, *args, **kwargs):
        """
        Perform a soft delete by setting is_deleted=True.
        """
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            logger.info("LeadViewSet.destroy: Soft-deleted Lead pk=%s.", instance.pk)
            return Response(status=drf_status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            logger.error(
                "LeadViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Lead. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LeadFollowUpViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lead Follow-Up history.

    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    Filter: leadid, leadstatusid, executiveid
    Search: actiontaken, remarks, executive_name
    Ordering: followupid, followupdate
    """
    queryset = LeadFollowUp.objects.select_related('leadid', 'leadstatusid').all()
    serializer_class = LeadFollowUpSerializer
    filterset_fields = ['leadid', 'leadstatusid', 'executiveid']
    search_fields = ['actiontaken', 'remarks', 'executive_name']
    ordering_fields = ['followupid', 'followupdate']
    ordering = ['followupid']

    # ✅ NEW — General Exception safety net for FollowUp deletes
    def destroy(self, request, *args, **kwargs):
        """
        Safety net for deleting a FollowUp record.
        Catches any unexpected DB or integrity errors and logs them.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "LeadFollowUpViewSet.destroy: ProtectedError — FollowUp pk=%s "
                "is protected. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Follow-Up record because it is referenced by other records."},
                status=drf_status.HTTP_409_CONFLICT,
            )
        except Exception as exc:
            logger.error(
                "LeadFollowUpViewSet.destroy: Unexpected error for pk=%s — %s",
                kwargs.get('pk'), exc, exc_info=True,
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the Follow-Up. Check server logs for details."},
                status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==============================================================================
# FRONTEND VIEWS (Bootstrap UI)
# ==============================================================================

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.db import DatabaseError
from .forms import RegionForm, ProductForm, LeadForm


class DashboardView(TemplateView):
    template_name = 'leads/dashboard.html'

    # ✅ NEW — wrap DB queries in try/except; DB failure won't crash the dashboard
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['total_leads']     = Lead.objects.filter(is_deleted=False).count()
            context['total_products']  = Product.objects.count()
            context['total_regions']   = Region.objects.count()
            context['total_followups'] = LeadFollowUp.objects.count()
            logger.info(
                "DashboardView: Stats fetched — leads=%s, products=%s, regions=%s, follow_ups=%s",
                context['total_leads'], context['total_products'],
                context['total_regions'], context['total_followups'],
            )
        except DatabaseError as exc:
            logger.error(
                "DashboardView.get_context_data: DB error while fetching stats — %s",
                exc, exc_info=True,
            )
            # Provide safe zero defaults so the template still renders
            context.setdefault('total_leads', 0)
            context.setdefault('total_products', 0)
            context.setdefault('total_regions', 0)
            context.setdefault('total_followups', 0)
        except Exception as exc:
            logger.error(
                "DashboardView.get_context_data: Unexpected error — %s",
                exc, exc_info=True,
            )
            context.setdefault('total_leads', 0)
            context.setdefault('total_products', 0)
            context.setdefault('total_regions', 0)
            context.setdefault('total_followups', 0)
        return context


class RegionListView(ListView):
    model = Region
    template_name = 'leads/region_list.html'
    context_object_name = 'regions'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(regionname__icontains=query)
        return queryset


class RegionCreateView(CreateView):
    model = Region
    form_class = RegionForm
    template_name = 'leads/region_form.html'
    success_url = reverse_lazy('leads:region_list')

    def form_valid(self, form):
        from django.utils import timezone
        form.instance.added_dts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        form.instance.added_by = self.request.user.get_full_name() or self.request.user.username
        messages.success(self.request, "Region added successfully!")
        return super().form_valid(form)


class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'leads/region_form.html'
    success_url = reverse_lazy('leads:region_list')

    def form_valid(self, form):
        messages.success(self.request, "Region updated successfully!")
        return super().form_valid(form)


class RegionDeleteView(DeleteView):
    model = Region
    template_name = 'leads/confirm_delete.html'
    success_url = reverse_lazy('leads:region_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Region'
        context['object_name'] = self.object.regionname
        context['cancel_url'] = reverse_lazy('leads:region_list')
        return context

    # ✅ EXISTING + ENHANCED — added general Exception fallback + logging
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            logger.info(
                "RegionDeleteView: Region '%s' (pk=%s) deleted successfully.",
                self.object.regionname, self.object.pk,
            )
            messages.success(request, "Region deleted successfully!")
            return redirect(self.success_url)
        except ProtectedError:
            logger.warning(
                "RegionDeleteView: ProtectedError — Region '%s' (pk=%s) is referenced "
                "by Territories or Leads. Delete blocked.",
                self.object.regionname, self.object.pk,
            )
            messages.error(
                request,
                f'Cannot delete Region "{self.object.regionname}" because it is referenced by '
                f'existing Territories or Leads. Please remove those records first.'
            )
            return redirect(self.success_url)
        except Exception as exc:
            logger.error(
                "RegionDeleteView: Unexpected error deleting Region '%s' (pk=%s) — %s",
                self.object.regionname, self.object.pk, exc, exc_info=True,
            )
            messages.error(
                request,
                f'An unexpected error occurred while deleting Region "{self.object.regionname}". '
                f'Please contact the administrator.'
            )
            return redirect(self.success_url)


class ProductListView(ListView):
    model = Product
    template_name = 'leads/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('categoryid')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(productname__icontains=query)
        if category:
            queryset = queryset.filter(categoryid=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'leads/product_form.html'
    success_url = reverse_lazy('leads:product_list')

    def form_valid(self, form):
        from django.utils import timezone
        form.instance.added_dts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        form.instance.added_by = self.request.user.get_full_name() or self.request.user.username
        messages.success(self.request, "Product added successfully!")
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'leads/product_form.html'
    success_url = reverse_lazy('leads:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully!")
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'leads/confirm_delete.html'
    success_url = reverse_lazy('leads:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Product'
        context['object_name'] = self.object.productname
        context['cancel_url'] = reverse_lazy('leads:product_list')
        return context

    # ✅ EXISTING + ENHANCED — added general Exception fallback + logging
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            logger.info(
                "ProductDeleteView: Product '%s' (pk=%s) deleted successfully.",
                self.object.productname, self.object.pk,
            )
            messages.success(request, "Product deleted successfully!")
            return redirect(self.success_url)
        except ProtectedError:
            logger.warning(
                "ProductDeleteView: ProtectedError — Product '%s' (pk=%s) is referenced "
                "by Leads. Delete blocked.",
                self.object.productname, self.object.pk,
            )
            messages.error(
                request,
                f'Cannot delete Product "{self.object.productname}" because it is referenced by '
                f'existing Leads. Please remove those leads first.'
            )
            return redirect(self.success_url)
        except Exception as exc:
            logger.error(
                "ProductDeleteView: Unexpected error deleting Product '%s' (pk=%s) — %s",
                self.object.productname, self.object.pk, exc, exc_info=True,
            )
            messages.error(
                request,
                f'An unexpected error occurred while deleting Product "{self.object.productname}". '
                f'Please contact the administrator.'
            )
            return redirect(self.success_url)


class LeadListView(ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        queryset = Lead.objects.select_related('productid', 'statusid').filter(is_deleted=False)
        query = self.request.GET.get('q')
        region = self.request.GET.get('region')
        status = self.request.GET.get('status')
        product = self.request.GET.get('product')

        if query:
            queryset = queryset.filter(
                Q(personname__icontains=query) |
                Q(companyname__icontains=query) |
                Q(email__icontains=query) |
                Q(contactno__icontains=query) |
                Q(city__icontains=query)
            )
        if region:
            queryset = queryset.filter(regionid=region)
        if status:
            queryset = queryset.filter(statusid=status)
        if product:
            queryset = queryset.filter(productid=product)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['statuses'] = LeadStatus.objects.all()
        context['products'] = Product.objects.all()
        return context


class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'
    success_url = reverse_lazy('leads:lead_list')

    def form_valid(self, form):
        from django.utils import timezone
        form.instance.added_dts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        form.instance.added_by = self.request.user.get_full_name() or self.request.user.username
        form.instance.lead_gen_date = timezone.now().date()
        messages.success(self.request, "Lead entry created successfully!")
        return super().form_valid(form)


class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'
    success_url = reverse_lazy('leads:lead_list')

    def form_valid(self, form):
        messages.success(self.request, "Lead updated successfully!")
        return super().form_valid(form)


class LeadDeleteView(DeleteView):
    model = Lead
    template_name = 'leads/confirm_delete.html'
    success_url = reverse_lazy('leads:lead_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Lead'
        context['object_name'] = self.object.personname
        context['cancel_url'] = reverse_lazy('leads:lead_list')
        return context

    # ✅ EXISTING + ENHANCED — added general Exception fallback + logging
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            person_name = self.object.personname
            self.object.is_deleted = True
            self.object.save()
            logger.info("LeadDeleteView: Lead '%s' (pk=%s) soft-deleted successfully.", person_name, self.object.pk)
            messages.success(request, "Lead deleted successfully!")
            return redirect(self.success_url)
        except ProtectedError:
            logger.warning(
                "LeadDeleteView: ProtectedError — Lead '%s' (pk=%s) is protected by "
                "other linked records. Delete blocked.", self.object.personname, self.object.pk,
            )
            messages.error(
                request,
                f'Cannot delete Lead "{self.object.personname}" because it is referenced by '
                f'other protected records in the database.'
            )
            return redirect(self.success_url)
        except Exception as exc:
            logger.error(
                "LeadDeleteView: Unexpected error deleting Lead '%s' (pk=%s) — %s",
                self.object.personname, self.object.pk, exc, exc_info=True,
            )
            messages.error(
                request,
                f'An unexpected error occurred while deleting Lead "{self.object.personname}". '
                f'Please contact the administrator.'
            )
            return redirect(self.success_url)


# ==============================================================================
# PRODUCT EXCEL UPLOAD VIEW
# ==============================================================================

import pandas as pd
from django.views import View
from django.utils import timezone


class ProductExcelUploadView(View):
    """
    Handles bulk product upload via an Excel (.xlsx / .xls) file.

    Expected columns (case-insensitive):
        productname  | category  | isactive

    Validation rules per row:
        1. productname must not be empty.
        2. category must not be empty and must match an existing ProductCategory.
        3. productname must not already exist in the DB (duplicate check).
        4. isactive defaults to 1 (True) when the cell is blank.
    """

    template_name = 'leads/product_excel_upload.html'

    def get(self, request):
        return self._render(request)

    def post(self, request):
        excel_file = request.FILES.get('excel_file')

        # ── 1. File presence check ──────────────────────────────────────────
        if not excel_file:
            messages.error(request, "Please select an Excel file before uploading.")
            return self._render(request)

        # ── 2. Extension check ──────────────────────────────────────────────
        if not (excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls')):
            messages.error(request, "Invalid file type. Please upload an Excel file (.xlsx or .xls).")
            return self._render(request)

        # ── 3. Parse Excel ──────────────────────────────────────────────────
        try:
            df = pd.read_excel(excel_file, dtype=str)
        except Exception as exc:
            logger.error("ProductExcelUploadView: Failed to parse Excel — %s", exc, exc_info=True)
            messages.error(request, f"Could not read the Excel file: {exc}")
            return self._render(request)

        # ── 4. Normalise column names (strip spaces, lowercase) ─────────────
        df.columns = [c.strip().lower().replace(' ', '') for c in df.columns]

        required_cols = {'productname', 'category', 'isactive'}
        missing = required_cols - set(df.columns)
        if missing:
            messages.error(
                request,
                f"Missing required column(s): {', '.join(missing)}. "
                "Please ensure your Excel file has columns: ProductName, Category, IsActive."
            )
            return self._render(request)

        # ── 5. Pre-load category map & existing product names ───────────────
        category_map = {
            cat.categoryname.strip().lower(): cat
            for cat in ProductCategory.objects.all()
        }
        existing_names = set(
            Product.objects.values_list('productname', flat=True)
        )
        # Track names already seen in this upload batch (prevent intra-batch duplicates)
        seen_in_batch = set()

        row_results = []   # list of dicts: {row, status, message}
        products_to_create = []
        added_by = request.user.get_full_name() or request.user.username
        added_dts = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        # ── 6. Row-level validation ─────────────────────────────────────────
        for idx, row in df.iterrows():
            row_num = idx + 2  # Excel row number (header = row 1)
            errors = []

            raw_name = str(row.get('productname', '') or '').strip()
            raw_cat  = str(row.get('category', '') or '').strip()
            raw_active = str(row.get('isactive', '') or '').strip()

            # Rule 1 — product name must not be empty
            if not raw_name or raw_name.lower() == 'nan':
                errors.append("Product Name is empty.")

            # Rule 3 — category must not be empty
            if not raw_cat or raw_cat.lower() == 'nan':
                errors.append("Category is empty.")

            if errors:
                row_results.append({
                    'row': row_num,
                    'status': 'error',
                    'product': raw_name or '(blank)',
                    'messages': errors,
                })
                continue

            # Rule 2 — duplicate check (DB + batch)
            name_key = raw_name.lower()
            if raw_name in existing_names or name_key in seen_in_batch:
                row_results.append({
                    'row': row_num,
                    'status': 'error',
                    'product': raw_name,
                    'messages': [f'Duplicate product name "{raw_name}" — already exists.'],
                })
                continue

            # Category lookup
            cat_key = raw_cat.lower()
            if cat_key not in category_map:
                row_results.append({
                    'row': row_num,
                    'status': 'error',
                    'product': raw_name,
                    'messages': [f'Category "{raw_cat}" does not exist. Please add it first.'],
                })
                continue

            # Rule 4 — isactive defaults to 1 if blank
            if not raw_active or raw_active.lower() in ('nan', ''):
                is_active_val = 1
            elif raw_active.lower() in ('true', '1', 'yes', 'active'):
                is_active_val = 1
            elif raw_active.lower() in ('false', '0', 'no', 'inactive'):
                is_active_val = 0
            else:
                is_active_val = 1  # default for unrecognised values

            # All checks passed — queue for insert
            seen_in_batch.add(name_key)
            products_to_create.append(Product(
                productname=raw_name,
                categoryid=category_map[cat_key],
                is_active=is_active_val,
                added_by=added_by,
                added_dts=added_dts,
            ))
            row_results.append({
                'row': row_num,
                'status': 'success',
                'product': raw_name,
                'messages': ['Ready for import.'],
            })

        # ── 7. Bulk insert valid rows ───────────────────────────────────────
        inserted_count = 0
        if products_to_create:
            try:
                Product.objects.bulk_create(products_to_create)
                inserted_count = len(products_to_create)
                logger.info(
                    "ProductExcelUploadView: Bulk inserted %d products by user '%s'.",
                    inserted_count, added_by,
                )
            except Exception as exc:
                logger.error(
                    "ProductExcelUploadView: bulk_create failed — %s", exc, exc_info=True,
                )
                messages.error(request, f"Database error during import: {exc}")
                return self._render(request)

        # ── 8. Summary flash message ────────────────────────────────────────
        error_count = sum(1 for r in row_results if r['status'] == 'error')
        if inserted_count:
            messages.success(
                request,
                f"{inserted_count} product(s) imported successfully."
                + (f" {error_count} row(s) had errors — see details below." if error_count else "")
            )
        else:
            messages.warning(request, "No products were imported. Please review the errors below.")

        return self._render(request, row_results=row_results)

    # ── Helper ──────────────────────────────────────────────────────────────
    def _render(self, request, row_results=None):
        from django.shortcuts import render
        return render(request, self.template_name, {
            'row_results': row_results or [],
            'categories': ProductCategory.objects.all(),
        })
