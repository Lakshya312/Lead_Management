from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from datetime import datetime

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