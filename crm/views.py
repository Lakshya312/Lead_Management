from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, LeadSerializer, RegionSerializer
from rest_framework import status
import getpass

'''FOR PRODUCTS'''
class Product_view:

    def product_list(request):
        products = Product.objects.all()
        form = ProductForm()

        return render(
            request,
            'product_list.html',
            {'products': products, 'form': form}
        )

    def add_product(request):

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

                return redirect('product_list')

        products = Product.objects.all()

        return render(
            request,
            'product_list.html',
            {'products': products, 'form': form}
        )

    def edit_product(request, productid):
        product = get_object_or_404(Product, pk=productid)
        form = ProductForm(request.POST or None, instance=product)

        if form.is_valid():
            product = form.save(commit=False)
            product.added_dts = datetime.now()
            product.save()
            return redirect('product_list')

        return render(request, 'product_list.html', {
            'products': Product.objects.all(),
            'form': form,
            'edit_mode': True
        })

    def delete_product(request, productid):
        product = get_object_or_404(Product, pk=productid)
        product.delete()
        return redirect('product_list')

'''FOR REGION'''

class Region_view:

    def region_list(request):

        regions = Region.objects.all()
        form = RegionForm()

        return render(
            request,
            'region_list.html',
            {
                'regions': regions,
                'form': form
            }
        )


    def add_region(request):

        if request.method == 'POST':

            form = RegionForm(request.POST)

            if form.is_valid():

                last_region = Region.objects.order_by(
                    '-regionid'
                ).first()

                region = form.save(commit=False)

                region.regionid = last_region.regionid + 1 if last_region else 1
                region.added_by = request.user.username if request.user.is_authenticated else 'System'
                region.added_dts = datetime.now()

                region.save()

                return redirect('region_list')

        return redirect('region_list')


    def edit_region(request, regionid):

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

            region.added_by = request.user.username if request.user.is_authenticated else 'System'

            region.save()

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


    def delete_region(request, regionid):

        region = get_object_or_404(
            Region,
            pk=regionid
        )

        region.delete()

        return redirect('region_list')

'''FOR LEAD'''
class Lead_view:
    def lead_list(request):
        leads = Lead.objects.all()
        form = LeadForm()
        return render(
            request,
            'lead_list.html',
            {
                'leads': leads,
                'form': form
            }
        )

    def add_lead(request):
        if request.method == 'POST':
            form = LeadForm(request.POST)
            if form.is_valid():
                last_lead = Lead.objects.order_by('-leadid').first()
                lead = form.save(commit=False)
                lead.leadid = last_lead.leadid + 1 if last_lead else 1
                
                # Auto audit tracking tags
                lead.added_by = request.user.username if request.user.is_authenticated else "System"
                lead.added_dts = datetime.now()
                
                lead.save()
                return redirect('lead_list')
            else:
                # If form validation fails, display errors right on the same master interface page
                leads = Lead.objects.all()
                return render(request, 'lead_list.html', {'leads': leads, 'form': form})
                
        return redirect('lead_list')

    def edit_lead(request, leadid):
        lead = get_object_or_404(Lead, pk=leadid)
        form = LeadForm(request.POST or None, instance=lead)

        if request.method == 'POST' and form.is_valid():
            lead = form.save(commit=False)
            lead.added_dts = datetime.now()
            form.save()
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

    def delete_lead(request, leadid):
        lead = get_object_or_404(Lead, pk=leadid)
        lead.delete()
        return redirect('lead_list')
    
'''DASHBOARD'''
def dashboard(request):
    return render(request, 'dashboard.html')

'''CREATE API VIEW'''

@api_view(['GET', 'POST'])
def product_api(request):

    if request.method == 'GET':

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            "success": True,
            "count": products.count(),
            "data": serializer.data
        })

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            last = Product.objects.order_by('-productid').first()
            print(request.user)
            print(request.user.is_authenticated)
            serializer.save(
                productid=last.productid + 1 if last else 1,
                added_by=request.user.username if request.user.is_authenticated else "System",
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

@api_view(['GET', 'POST'])
def lead_api(request):

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
        serializer.save(
            leadid=last.leadid + 1 if last else 1,
            added_by=request.user.username if request.user.is_authenticated else "System",
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

@api_view(['GET', 'POST'])
def region_api(request):

    if request.method == 'GET':
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response({
            "success": True,
            "count": regions.count(),
            "data": serializer.data
        })

    serializer = RegionSerializer(data=request.data)

    if serializer.is_valid():
        last = Region.objects.order_by('-regionid').first()
        serializer.save(
            regionid=last.regionid + 1 if last else 1,
            added_by=request.user.username if request.user.is_authenticated else "System",
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