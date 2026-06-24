from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, LeadSerializer, RegionSerializer
from rest_framework import status
import getpass
from .utils import log_error

'''FOR PRODUCTS'''
class Product_view:

    def product_list(request):

        search = request.GET.get('search', '')

        products = Product.objects.select_related(
            'categoryid'
        )

        if search:

            if search.isdigit():

                products = products.filter(
                    productid=int(search)
                )

            else:

                products = products.filter(
                    productname__icontains=search
                )

        form = ProductForm()

        return render(
            request,
            'product_list.html',
            {
                'products': products,
                'form': form,
                'search': search
            }
        )

    @staticmethod
    def add_product(request):

        try:

            if request.method == 'POST':

                form = ProductForm(request.POST)

                if form.is_valid():

                    last_product = Product.objects.order_by(
                        '-productid'
                    ).first()

                    product = form.save(commit=False)

                    product.productid = (
                        last_product.productid + 1
                        if last_product
                        else 1
                    )

                    product.added_dts = datetime.now()

                    product.added_by = (
                        request.user.username
                        if request.user.is_authenticated
                        else "System"
                    )

                    product.save()

                    messages.success(
                        request,
                        "Product added successfully."
                    )

                    return redirect('product_list')

            products = Product.objects.all()

            return render(
                request,
                'product_list.html',
                {
                    'products': products,
                    'form': form
                }
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

            return redirect('product_list')

    @staticmethod
    def edit_product(request, productid):

        try:

            product = get_object_or_404(
                Product,
                pk=productid
            )

            form = ProductForm(
                request.POST or None,
                instance=product
            )

            if form.is_valid():

                product = form.save(commit=False)

                product.added_dts = datetime.now()

                product.save()

                messages.success(
                    request,
                    "Product updated successfully."
                )

                return redirect('product_list')

            return render(
                request,
                'product_list.html',
                {
                    'products': Product.objects.all(),
                    'form': form,
                    'edit_mode': True
                }
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

            return redirect('product_list')

    @staticmethod
    def delete_product(request, productid):

        try:

            product = get_object_or_404(
                Product,
                pk=productid
            )

            product.delete()

            messages.success(
                request,
                "Product deleted successfully."
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

        return redirect('product_list')

'''FOR REGION'''

class Region_view:

    def region_list(request):

        search = request.GET.get('search', '')

        regions = Region.objects.all()

        if search:

            if search.isdigit():

                regions = regions.filter(
                    regionid=int(search)
                )

            else:

                regions = regions.filter(
                    regionname__istartswith=search
                )

        form = RegionForm()

        return render(
            request,
            'region_list.html',
            {
                'regions': regions,
                'form': form,
                'search': search
            }
        )

    @staticmethod
    def add_region(request):

        try:

            if request.method == 'POST':

                form = RegionForm(request.POST)

                if form.is_valid():

                    last_region = Region.objects.order_by(
                        '-regionid'
                    ).first()

                    region = form.save(commit=False)

                    region.regionid = (
                        last_region.regionid + 1
                        if last_region else 1
                    )

                    region.added_by = (
                        request.user.username
                        if request.user.is_authenticated
                        else 'System'
                    )

                    region.added_dts = datetime.now()

                    region.save()

                    messages.success(
                        request,
                        "Region added successfully."
                    )

                    return redirect('region_list')

            return redirect('region_list')

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

            return redirect('region_list')


    @staticmethod
    def edit_region(request, regionid):

        try:

            region = get_object_or_404(
                Region,
                pk=regionid
            )

            form = RegionForm(
                request.POST or None,
                instance=region
            )

            if request.method == 'POST' and form.is_valid():

                region = form.save(commit=False)

                region.added_dts = datetime.now()

                region.added_by = (
                    request.user.username
                    if request.user.is_authenticated
                    else 'System'
                )

                region.save()

                messages.success(
                    request,
                    "Region updated successfully."
                )

                return redirect('region_list')

            regions = Region.objects.all()

            return render(
                request,
                'region_list.html',
                {
                    'regions': regions,
                    'form': form,
                    'edit_mode': True
                }
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

            return redirect('region_list')


    @staticmethod
    def delete_region(request, regionid):

        try:

            region = get_object_or_404(
                Region,
                pk=regionid
            )

            region.delete()

            messages.success(
                request,
                "Region deleted successfully."
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

        return redirect('region_list')

'''FOR LEAD'''
class Lead_view:
    def lead_list(request):

        search = request.GET.get('search', '')

        leads = Lead.objects.select_related(
            'productid',
            'regionid',
            'statusid',
            'leadsourceid'
        )

        if search:

            if search.isdigit():

                leads = leads.filter(
                    leadid=int(search)
                )

            else:

                leads = leads.filter(

                    Q(personname__istartswith=search) |
                    Q(productid__productname__icontains=search) |
                    Q(regionid__regionname__istartswith=search)

                )

        form = LeadForm()

        return render(
            request,
            'lead_list.html',
            {
                'leads': leads,
                'form': form,
                'search': search
            }
        )

    @staticmethod
    def add_lead(request):

        try:
            if request.method == 'POST':

                form = LeadForm(request.POST)

                if form.is_valid():

                    last_lead = Lead.objects.order_by('-leadid').first()

                    lead = form.save(commit=False)

                    lead.leadid = (
                        last_lead.leadid + 1
                        if last_lead else 1
                    )

                    lead.added_by = (
                        request.user.username
                        if request.user.is_authenticated
                        else "System"
                    )

                    lead.added_dts = datetime.now()

                    lead.save()

                    messages.success(
                        request,
                        "Lead added successfully."
                    )

                    return redirect('lead_list')

                leads = Lead.objects.all()

                return render(
                    request,
                    'lead_list.html',
                    {
                        'leads': leads,
                        'form': form
                    }
                )

            return redirect('lead_list')

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

            return redirect('lead_list')

    @staticmethod
    def edit_lead(request, leadid):

        try:

            lead = get_object_or_404(
                Lead,
                pk=leadid
            )

            form = LeadForm(
                request.POST or None,
                instance=lead
            )

            if request.method == 'POST' and form.is_valid():

                lead = form.save(commit=False)

                lead.added_dts = datetime.now()
                lead.save()

                messages.success(
                    request,
                    "Lead updated successfully."
                )

                return redirect('lead_list')

            leads = Lead.objects.all()

            return render(
                request,
                'lead_list.html',
                {
                    'leads': leads,
                    'form': form,
                    'edit_mode': True
                }
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

        return redirect('lead_list')

    @staticmethod
    def delete_lead(request, leadid):

        try:

            lead = get_object_or_404(
                Lead,
                pk=leadid
            )

            lead.delete()

            messages.success(
                request,
                "Lead deleted successfully."
            )

        except Exception as e:

            log_error(e)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )

        return redirect('lead_list')
    
'''DASHBOARD'''
def dashboard(request):
    return render(request, 'dashboard.html')

'''CREATE API VIEW'''

@api_view(['GET', 'POST'])
def product_api(request):

    try:

        if request.method == 'GET':

            products = Product.objects.all()

            serializer = ProductSerializer(
                products,
                many=True
            )

            return Response({
                "success": True,
                "count": products.count(),
                "data": serializer.data
            })

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            last = Product.objects.order_by(
                '-productid'
            ).first()

            serializer.save(
                productid=last.productid + 1 if last else 1,
                added_by=getpass.getuser(),
                added_dts=datetime.now()
            )

            return Response({
                "success": True,
                "message": "Product added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        log_error(e)

        return Response({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def lead_api(request):

    try:

        if request.method == 'GET':
            leads = Lead.objects.all()
            serializer = LeadSerializer(leads, many=True)

            return Response({
                "success": True,
                "count": leads.count(),
                "data": serializer.data
            })

        serializer = LeadSerializer(data=request.data)

        if serializer.is_valid():

            last = Lead.objects.order_by('-leadid').first()
            int("abc")
            serializer.save(
                leadid=last.leadid + 1 if last else 1,
                added_by=getpass.getuser(),
                added_dts=datetime.now()
            )

            return Response({
                "success": True,
                "message": "Lead added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        log_error(e)

        return Response({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def region_api(request):

    try:

        if request.method == 'GET':

            regions = Region.objects.all()

            serializer = RegionSerializer(
                regions,
                many=True
            )

            return Response({
                "success": True,
                "count": regions.count(),
                "data": serializer.data
            })

        serializer = RegionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            last = Region.objects.order_by(
                '-regionid'
            ).first()

            serializer.save(
                regionid=last.regionid + 1 if last else 1,
                added_by=getpass.getuser(),
                added_dts=datetime.now()
            )

            return Response({
                "success": True,
                "message": "Region added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        log_error(e)

        return Response({
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# PUT APIs
@api_view(['PUT'])
def update_product_api(request, productid):
    product = get_object_or_404(Product, pk=productid)
    before = ProductSerializer(product).data
    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Product updated successfully.",
            "before": before,
            "after": serializer.data
        })

    return Response({
        "success": False,
        "message": "Validation failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_region_api(request, regionid):
    region = get_object_or_404(Region, pk=regionid)
    before = RegionSerializer(region).data
    serializer = RegionSerializer(region, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Region updated successfully.",
            "before": before,
            "after": serializer.data
        })

    return Response({
        "success": False,
        "message": "Validation failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_lead_api(request, leadid):
    lead = get_object_or_404(Lead, pk=leadid)
    before = LeadSerializer(lead).data
    serializer = LeadSerializer(lead, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Lead updated successfully.",
            "before": before,
            "after": serializer.data
        })

    return Response({
        "success": False,
        "message": "Validation failed.",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# DELETE APIs
@api_view(['DELETE'])
def delete_product_api(request, productid):
    product = get_object_or_404(Product, pk=productid)
    deleted_data = ProductSerializer(product).data
    product.delete()

    return Response({
        "success": True,
        "message": "Product deleted successfully.",
        "data": deleted_data
    })

@api_view(['DELETE'])
def delete_region_api(request, regionid):
    region = get_object_or_404(Region, pk=regionid)
    deleted_data = RegionSerializer(region).data
    region.delete()

    return Response({
        "success": True,
        "message": "Region deleted successfully.",
        "data": deleted_data
    })

@api_view(['DELETE'])
def delete_lead_api(request, leadid):
    lead = get_object_or_404(Lead, pk=leadid)
    deleted_data = LeadSerializer(lead).data
    lead.delete()

    return Response({
        "success": True,
        "message": "Lead deleted successfully.",
        "data": deleted_data
    })

# LEAD VALIDATIONS
def check_personname(request):
    personname = request.GET.get('personname')

    exists = Lead.objects.filter(
        personname=personname
    ).exists()

    return JsonResponse({
        'exists': exists
    })

def check_contactno(request):
    contactno = request.GET.get('contactno')

    exists = Lead.objects.filter(
        contactno=contactno
    ).exists()

    return JsonResponse({
        'exists': exists
    })

def check_email(request):
    email = request.GET.get('email')

    exists = Lead.objects.filter(
        email=email
    ).exists()

    return JsonResponse({
        'exists': exists
    })

# PRODUCT VALIDATIONS
def check_productname(request):
    productname = request.GET.get('productname')

    exists = Product.objects.filter(
        productname=productname
    ).exists()

    return JsonResponse({
        'exists': exists
    })

# REGION VALIDATIONS
def check_regionname(request):
    regionname = request.GET.get('regionname')
    print("REGION =", regionname)
    exists = Region.objects.filter(
        regionname=regionname
    ).exists()
    print("EXIST", exists)
    return JsonResponse({
        'exists': exists
    })