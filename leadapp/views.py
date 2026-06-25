from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Region ,Lead ,ProductCategory
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
import logging
logger = logging.getLogger("leadapp")
from .forms import ProductUploadForm
from django.db.models import Q  
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(
                request,
                user
            )
            return redirect("home")
        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )
    return render(
        request,
        "login.html"
    )

def logout_view(request):

    logout(request)

    return redirect("login")

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

            try:
                serializer.save(
                Added_By=getpass.getuser(),
                Added_Dts=timezone.now()
            )
            except Exception as e:
                logger.error(
                    f"Product Save Error: {str(e)}"
                )
                return Response(
                    {
                        "Success": False,
                        "Message": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
            return Response(
                {
                    "Success": True,
                    "Message": "Product Created Successfully",
                    "Data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

    logger.error(
        f"Product Validation Error: {serializer.errors}"
    )

    return Response(
        {
            "Success": False,
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
    
@login_required   
def home(request):
    product_count = Product.objects.count()
    region_count = Region.objects.count()
    lead_count = Lead.objects.count()
    try:
        x = 10 / 0
    except Exception as e:
        logger.error(f"Test Error: {str(e)}")

    return render(request, "home.html",{
        "product_count": product_count,
        "region_count": region_count,
        "lead_count": lead_count
    })

@login_required
def product_list(request):

    search = request.GET.get("search", "")

    products = Product.objects.all()

    if search:

        query = Q(
            ProductName__icontains=search
        )

        if search.isdigit():

            query |= Q(
                ProductID=int(search)
            )

        products = products.filter(query)

    return render(
        request,
        "product_list.html",
        {
            "products": products
        }
    )

@login_required
def product_add(request):

    form = ProductForm(
        request.POST or None
    )

    if form.is_valid():

        try:

            product = form.save(
                commit=False
            )

            product.Added_By = getpass.getuser()

            product.Added_Dts = timezone.now()

            product.save()

            return redirect(
                "product_list"
            )

        except Exception as e:

            logger.error(
                f"Product Save Error: {str(e)}"
            )

    return render(
        request,
        "product_form.html",
        {"form": form}
    )

@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def product_bulk_upload(request):

    if request.method == "POST":

        form = ProductUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            excel_file = request.FILES["excel_file"]

            df = pd.read_excel(excel_file)

            errors = []

            # -----------------------------
            # FIRST LOOP : ONLY VALIDATION
            # -----------------------------
            for index, row in df.iterrows():

                product_name = str(
                    row["ProductName"]
                ).strip()

                category_name = str(
                    row["Category"]
                ).strip()

                # Validation 1
                if pd.isna(row["ProductName"]) or product_name == "":

                    errors.append(
                        f"Row {index+2}: Product Name cannot be empty."
                    )

                # Validation 2
                elif Product.objects.filter(
                    ProductName__iexact=product_name
                ).exists():

                    errors.append(
                        f"Row {index+2}: '{product_name}' already exists."
                    )

                # Validation 3
                elif pd.isna(row["Category"]) or category_name == "":

                    errors.append(
                        f"Row {index+2}: Category cannot be empty."
                    )

                else:

                    if not ProductCategory.objects.filter(
                        CategoryName=category_name
                    ).exists():

                        errors.append(
                            f"Row {index+2}: Category '{category_name}' does not exist."
                        )

            # -----------------------------
            # IF ERRORS FOUND
            # -----------------------------
            if errors:

                for error in errors:
                  return render(
        request,
        "product_bulk_upload.html",
        {
            "form": form,
            "errors": errors
        }
    )

            # -----------------------------
            # SECOND LOOP : INSERT DATA
            # -----------------------------
            for index, row in df.iterrows():

                category = ProductCategory.objects.get(
                    CategoryName=row["Category"]
                )

                is_active = row["IsActive"]

                if pd.isna(is_active):

                    is_active = True

                Product.objects.create(

                    ProductName=row["ProductName"].strip(),

                    CategoryID=category,

                    Is_Active=is_active,

                    Added_By=getpass.getuser(),

                    Added_Dts=timezone.now()

                )

            messages.success(
                request,
                "Products Uploaded Successfully."
            )

            return redirect(
                "product_list"
            )

    else:

        form = ProductUploadForm()

    return render(
        request,
        "product_bulk_upload.html",
        {
            "form": form
        }
    )