from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer

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

@api_view(['GET'])
def product_api(request):

    products = Product.objects.all()

    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response(
        serializer.data
    )