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
    ).all()
    serializer_class = LeadSerializer
    filterset_fields = [
        'regionid', 'statusid', 'leadsourceid',
        'productid', 'territoryid', 'gender',
    ]
    search_fields = ['personname', 'companyname', 'email', 'contactno', 'city']
    ordering_fields = ['leadid', 'personname', 'companyname', 'lead_gen_date']
    ordering = ['leadid']

    # ✅ NEW — ProtectedError when Lead has existing FollowUp records
    def destroy(self, request, *args, **kwargs):
        """
        Block deletion if this Lead has existing LeadFollowUp records.
        Returns HTTP 409 instead of letting Django raise an unhandled ProtectedError (500).
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            logger.warning(
                "LeadViewSet.destroy: ProtectedError — Lead pk=%s has existing "
                "FollowUp records. Delete blocked.",
                kwargs.get('pk'),
            )
            return Response(
                {"error": "Cannot delete this Lead because it has existing Follow-Up records. Remove those follow-ups first."},
                status=drf_status.HTTP_409_CONFLICT,
            )
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
            context['total_leads'] = Lead.objects.count()
            context['total_products'] = Product.objects.count()
            context['total_regions'] = Region.objects.count()
            logger.info(
                "DashboardView: Stats fetched — leads=%s, products=%s, regions=%s",
                context['total_leads'], context['total_products'], context['total_regions'],
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
        except Exception as exc:
            logger.error(
                "DashboardView.get_context_data: Unexpected error — %s",
                exc, exc_info=True,
            )
            context.setdefault('total_leads', 0)
            context.setdefault('total_products', 0)
            context.setdefault('total_regions', 0)
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
        queryset = super().get_queryset().select_related('productid', 'statusid')
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
            self.object.delete()
            logger.info(
                "LeadDeleteView: Lead '%s' (pk=%s) deleted successfully.",
                self.object.personname, self.object.pk,
            )
            messages.success(request, "Lead deleted successfully!")
            return redirect(self.success_url)
        except ProtectedError:
            logger.warning(
                "LeadDeleteView: ProtectedError — Lead '%s' (pk=%s) has existing "
                "FollowUp records. Delete blocked.",
                self.object.personname, self.object.pk,
            )
            messages.error(
                request,
                f'Cannot delete Lead "{self.object.personname}" because it has existing Follow-Up records. '
                f'Please remove those follow-ups first.'
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
