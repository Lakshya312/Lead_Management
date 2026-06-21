from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Region ,Lead
from .forms import ProductForm, RegionForm ,LeadForm
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    ProductSerializer,
    RegionSerializer,
    LeadSerializer
)
import getpass
from django.db.models import Q  

@api_view(['GET', 'POST'])
def product_api(request):

    if request.method == 'GET':

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            "Success": True,
            "Count": products.count(),
            "Data": serializer.data
        })

    elif request.method == 'POST':

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                Added_By=getpass.getuser(),
                Added_Dts=timezone.now()
            )

            return Response(
                {
                    "Success": True,
                    "Message": "Product Created Successfully",
                    "Data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "Success": False,
                "Message": "Validation Failed",
                "Errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api(request, pk):

    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:

        return Response(
            {
                "Success": False,
                "Message": "Product Not Found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = ProductSerializer(product)

        return Response({
            "Success": True,
            "Message": "Product Retrieved Successfully",
            "Data": serializer.data
        })

    elif request.method == 'PUT':

        old_data = ProductSerializer(product).data

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "Success": True,
                "Message": "Product Updated Successfully",
                "Before_Update": old_data,
                "After_Update": serializer.data
            })

        return Response(
            {
                "Success": False,
                "Message": "Validation Failed",
                "Errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        deleted_data = ProductSerializer(product).data

        product.delete()

        return Response({
            "Success": True,
            "Message": "Product Deleted Successfully",
            "Deleted_Data": deleted_data
        })

@api_view(['GET', 'POST'])
def region_api(request):

    if request.method == 'GET':

        regions = Region.objects.all()

        serializer = RegionSerializer(
            regions,
            many=True
        )

        return Response(
            {
            "Success": True,
             "Count": regions.count(),
             "data":serializer.data
             })
    
    elif request.method == 'POST':

        serializer = RegionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
    Added_By=getpass.getuser(),
    Added_Dts=timezone.now()
)

            return Response({
         "Success":True,
         "message":"Region Created",
         "data": serializer.data})

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'DELETE'])
def region_detail_api(request, pk):

    try:
        region = Region.objects.get(pk=pk)

    except Region.DoesNotExist:

        return Response(
            {
                "Success": False,
                "Message": "Region Not Found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = RegionSerializer(region)

        return Response({
            "Success": True,
            "Message": "Region Retrieved Successfully",
            "Data": serializer.data
        })

    elif request.method == 'PUT':

        old_data = RegionSerializer(region).data

        serializer = RegionSerializer(
            region,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "Success": True,
                "Message": "Region Updated Successfully",
                "Before_Update": old_data,
                "After_Update": serializer.data
            })

        return Response(
            {
                "Success": False,
                "Message": "Validation Failed",
                "Errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        deleted_data = RegionSerializer(region).data

        region.delete()

        return Response({
            "Success": True,
            "Message": "Region Deleted Successfully",
            "Deleted_Data": deleted_data
        })

@api_view(['GET', 'POST'])
def lead_api(request):

    if request.method == 'GET':

        leads = Lead.objects.all()

        serializer = LeadSerializer(
            leads,
            many=True
        )

        return Response(
            {
            "Success": True,
             "Count": leads.count(),
             "data":serializer.data
             })

    elif request.method == 'POST':

        serializer = LeadSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                    Added_By=getpass.getuser(),
                    Added_Dts=timezone.now()
                )

            return Response({
                "Success":True,
                "message":"Lead Created",
                "data": serializer.data})

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'DELETE'])
def lead_detail_api(request, pk):

    try:
        lead = Lead.objects.get(pk=pk)

    except Lead.DoesNotExist:

        return Response(
            {
                "Success": False,
                "Message": "Lead Not Found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = LeadSerializer(lead)

        return Response({
            "Success": True,
            "Message": "Lead Retrieved Successfully",
            "Data": serializer.data
        })

    elif request.method == 'PUT':

        old_data = LeadSerializer(lead).data

        serializer = LeadSerializer(
            lead,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "Success": True,
                "Message": "Lead Updated Successfully",
                "Before_Update": old_data,
                "After_Update": serializer.data
            })

        return Response(
            {
                "Success": False,
                "Message": "Validation Failed",
                "Errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        deleted_data = LeadSerializer(lead).data

        lead.delete()

        return Response({
            "Success": True,
            "Message": "Lead Deleted Successfully",
            "Deleted_Data": deleted_data
        })
    
def home(request):
    return render(request, "home.html")
# PRODUCT CRUD

def product_list(request):
    search = request.GET.get("search", "")
    products = Product.objects.all()
    if search:
        products = products.filter(
            Q(ProductName__icontains=search) |
            Q(ProductID__icontains=search)
        )
        
    return render(request, "product_list.html", {"products": products})

def product_add(request):

    form = ProductForm(request.POST or None)

    if form.is_valid():

        product = form.save(commit=False)

        product.Added_By = getpass.getuser()
        product.Added_Dts = timezone.now()

        product.save()

        return redirect("product_list")

    return render(
        request,
        "product_form.html",
        {"form": form}
    )


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if form.is_valid():
        form.save()
        return redirect("product_list")

    return render(request, "product_form.html", {"form": form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(
        request,
        "confirm_delete.html",
        {"object": product}
    )


# REGION CRUD

def region_list(request):
    search = request.GET.get("search", "")
    regions = Region.objects.all()
    if search:
        regions = regions.filter(
            Q(RegionName__icontains=search) |
            Q(RegionID__icontains=search)
        )

    return render(
        request,
        "region_list.html",
        {"regions": regions}
    )


def region_add(request):

    form = RegionForm(request.POST or None)

    if form.is_valid():

        region = form.save(commit=False)

        region.Added_By = getpass.getuser()
        region.Added_Dts = timezone.now()

        region.save()

        return redirect("region_list")

    return render(
        request,
        "region_form.html",
        {"form": form}
    )

def region_edit(request, pk):
    region = get_object_or_404(
        Region,
        pk=pk
    )

    form = RegionForm(
        request.POST or None,
        instance=region
    )

    if form.is_valid():
        form.save()
        return redirect("region_list")

    return render(
        request,
        "region_form.html",
        {"form": form}
    )


def region_delete(request, pk):
    region = get_object_or_404(
        Region,
        pk=pk
    )

    if request.method == "POST":
        region.delete()
        return redirect("region_list")

    return render(
        request,
        "confirm_delete.html",
        {"object": region}
    )

def lead_list(request):
    search = request.GET.get("search","")
    leads = Lead.objects.all()
    if search:
        leads = leads.filter(
            Q(PersonName__icontains=search) |
            Q(LeadID__icontains=search)
        )
  
    return render(
        request,
        "lead_list.html",
        {"leads": leads}
    )

def lead_add(request):

    form = LeadForm(request.POST or None)

    if form.is_valid():

        lead = form.save(commit=False)

        lead.Added_By = getpass.getuser()
        lead.Added_Dts = timezone.now()

        lead.save()

        return redirect("lead_list")

    return render(
        request,
        "lead_form.html",
        {"form": form}
    )

def lead_edit(request, pk):

    lead = Lead.objects.get(pk=pk)

    form = LeadForm(
        request.POST or None,
        instance=lead
    )

    if form.is_valid():

        form.save()

        return redirect("lead_list")

    return render(
        request,
        "lead_form.html",
        {"form": form}
    )
def lead_delete(request, pk):

    lead = Lead.objects.get(pk=pk)

    if request.method == "POST":

        lead.delete()

        return redirect("lead_list")

    return render(
        request,
        "confirm_delete.html",
        {"object": lead}
    )