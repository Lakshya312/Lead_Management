from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Region
from .forms import ProductForm, RegionForm
from datetime import datetime

'''FOR PRODUCTS'''

# 1. MAIN LIST VIEW (GET ONLY)
def product_list(request):
    products = Product.objects.all()
    form = ProductForm()

    return render(
        request,
        'product_list.html',
        {'products': products, 'form': form}
    )

# 2. DEDICATED ADD VIEW (POST ONLY)
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

# 3. DEDICATED EDIT VIEW
def edit_product(request, productid):
    product = get_object_or_404(Product, pk=productid)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')

    # Keep the table loaded underneath the form while editing on the same page
    products = Product.objects.all()
    return render(
        request, 
        'product_list.html', 
        {'products': products, 'form': form, 'edit_mode': True}
    )

# 4. DEDICATED DELETE VIEW
def delete_product(request, productid):
    product = get_object_or_404(Product, pk=productid)
    product.delete()
    return redirect('product_list')

'''FOR REGION'''

# Python

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

            region.regionid = (
                last_region.regionid + 1
                if last_region
                else 1
            )

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

        form.save()

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