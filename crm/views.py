from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, LeadSerializer, RegionSerializer
from rest_framework import status
import getpass
from .utils import log_error
import json
from django.views.decorators.http import require_POST
import pandas as pd

@login_required(login_url='login')
def import_products(request):
    if request.method != 'POST':
        return redirect('product_list')

    uploaded_file = request.FILES.get('product_file')

    if not uploaded_file:
        messages.error(request, "Please select a file.")
        return redirect('product_list')

    try:
        # 1. Parse File Engine
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            messages.error(request, "Only CSV and Excel files are allowed.")
            return redirect('product_list')

        # Standardize expected headers to avoid column mismatch errors
        required_columns = ['ProductName', 'CategoryID', 'Is_Active']
        if not all(col in df.columns for col in required_columns):
            messages.error(request, "Missing required columns: ProductName, CategoryID, or Is_Active")
            return redirect('product_list')

        last_product = Product.objects.order_by('-productid').first()
        next_id = last_product.productid + 1 if last_product else 1

        imported = 0
        skipped = 0
        errors = []
        
        for index, row in df.iterrows():
            # Clean text properties and handle NaN cases safely
            product_name = str(row['ProductName']).strip() if pd.notna(row['ProductName']) else ""
            category_id = row['CategoryID']
            is_active = row['Is_Active']

            row_num = index + 2  # Human-readable row index layout line position

            # 2. Strict Validations
            if not product_name or product_name.lower() == "nan":
                errors.append(f"Row {row_num}: Empty Product Name")
                skipped += 1
                continue

            if not re.match(r'^[A-Za-z0-9 ]+$', product_name):
                errors.append(f"Row {row_num}: Invalid characters in Product Name ('{product_name}')")
                skipped += 1
                continue

            # Check if category ID is a valid number, then parse to integer safely
            if pd.isna(category_id) or not str(category_id).strip().replace('.0', '').isdigit():
                errors.append(f"Row {row_num}: Invalid Category ID mapping format")
                skipped += 1
                continue
            category_id = int(float(category_id))

            if not ProductCategory.objects.filter(categoryid=category_id).exists():
                errors.append(f"Row {row_num}: Category ID {category_id} does not exist in the database")
                skipped += 1
                continue

            # Normalize Is_Active from floats or strings safely
            if pd.isna(is_active) or str(is_active).strip().replace('.0', '') not in ['0', '1']:
                errors.append(f"Row {row_num}: Invalid Is_Active status value (must be 0 or 1)")
                skipped += 1
                continue
            is_active = int(float(is_active))

            if Product.objects.filter(productname__iexact=product_name).exists():
                errors.append(f"Row {row_num}: Duplicate Product Name ('{product_name}') detected")
                skipped += 1
                continue

            # 3. Create Record (Let DB auto-increment handle productid automatically)
            Product.objects.create(
                productid=next_id,
                productname=product_name,
                categoryid_id=category_id,
                is_active=is_active,
                added_by=request.user.username,
                added_dts=datetime.now()
            )
            imported += 1
            next_id+=1

        # Flash success/warning message summary counts instantly
        if imported > 0:
            messages.success(request, f"Successfully imported {imported} products into core matrix.")
        if skipped > 0:
            messages.warning(request, f"Skipped {skipped} rows due to validation conflicts.")

        # Save summary to session safely
        request.session['import_summary'] = {
            'imported': imported,
            'skipped': skipped,
            'errors': errors
        }

    except Exception as e:
        log_error(e)
        # Fallback log wrapper handle
        print(f"CRITICAL BULK IMPORT ERROR: {str(e)}")
        messages.error(request, "Something went wrong during data stream import parsing.")

    return redirect('product_list')

'''FOR LOGIN'''

class Login_view:
    def login_view(request):

        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:

                login(request, user)

                return redirect('dashboard')

            messages.error(
                request,
                'Invalid username or password.'
            )

        return render(
            request,
            'login.html'
        )

'''FOR LOGOUT'''

class Logout_view:
    def logout_view(request):

        logout(request)

        return redirect('login')

'''FOR PRODUCTS'''
class Product_view:
    @login_required(login_url='login')
    def product_list(request):
        search = request.GET.get('search', '')
        products = Product.objects.select_related('categoryid')

        if search:
            if search.isdigit():
                products = products.filter(productid=int(search))
            else:
                products = products.filter(productname__icontains=search)

        # 1. Handle Inline Asynchronous Form Record Add Submissions
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                try:
                    # Calculate the manual sequential primary key for your SQL Server setup
                    last_product = Product.objects.order_by('-productid').first()
                    next_id = last_product.productid + 1 if last_product else 1
                    
                    new_prod = form.save(commit=False)
                    new_prod.productid = next_id
                    new_prod.added_by = request.user.username
                    new_prod.added_dts = datetime.now()
                    new_prod.save()

                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'product': {
                                'id': new_prod.productid,
                                'name': new_prod.productname,
                                'category': new_prod.categoryid.categoryname if new_prod.categoryid else "N/A",
                                'is_active': getattr(new_prod, 'is_active', 1), # Fallback safety default
                                'added_by': new_prod.added_by,
                                'added_dts': new_prod.added_dts.strftime("%m/%d/%Y")
                            }
                        })
                    
                    messages.success(request, "Product added successfully.")
                    return redirect('product_list')
                    
                except Exception as e:
                    log_error(e)
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': str(e)}, status=500)
                    messages.error(request, "Error saving product down to database.")
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)

        else:
            # Instantiates a clean fallback structure on a default GET request routing loop
            form = ProductForm()

        import_summary = request.session.pop('import_summary', None)
        
        return render(
            request,
            'product_list.html',
            {
                'products': products,
                'form': form,
                'search': search,
                'import_summary': import_summary
            }
        )

    @login_required(login_url='login')
    @staticmethod # Keeps your staticmethod decorator intact
    def add_product(request):
        try:
            if request.method == 'POST':
                form = ProductForm(request.POST)

                if form.is_valid():
                    last_product = Product.objects.order_by('-productid').first()
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

                    # ==========================================
                    # NEW: ASYNC AJAX FETCH INTERCEPTOR HANDLER
                    # ==========================================
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'product': {
                                'id': product.productid,
                                'name': product.productname,
                                'category': product.categoryid.categoryname if product.categoryid else "N/A",
                                'is_active': getattr(product, 'is_active', 1), # Safely tracks 1 or 0
                                'added_by': product.added_by,
                                'added_dts': product.added_dts.strftime("%m/%d/%Y")
                            }
                        })

                    # Fallback for standard traditional form reloads
                    messages.success(request, "Product added successfully.")
                    return redirect('product_list')
                
                else:
                    # If form is invalid and it's an AJAX call, return errors
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': 'Invalid data formats.'}, status=400)

            # Fallback render block for GET requests or fallback sequences
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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': f"{type(e).__name__}: {str(e)}"}, status=500)

            messages.error(
                request,
                f"{type(e).__name__}: {str(e)}"
            )
            return redirect('product_list')

    @login_required(login_url='login')
    @staticmethod # Keeps your staticmethod decorator intact
    def edit_product(request, productid):
        try:
            product = get_object_or_404(Product, pk=productid)

            form = ProductForm(request.POST or None, instance=product)

            if request.method == 'POST':
                if form.is_valid():
                    product = form.save(commit=False)
                    product.added_dts = datetime.now()
                    product.save()

                    # ==========================================
                    # ASYNC AJAX FETCH INTERCEPTOR HANDLER
                    # ==========================================
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'product': {
                                'id': product.productid,
                                'name': product.productname,
                                'category': product.categoryid.categoryname if product.categoryid else "N/A",
                                'is_active': getattr(product, 'is_active', 1),
                                'added_by': product.added_by if product.added_by else "System",
                                'added_dts': product.added_dts.strftime("%m/%d/%Y")
                            }
                        })

                    messages.success(request, "Product updated successfully.")
                    return redirect('product_list')
                
                else:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': 'Invalid layout form data details.'}, status=400)

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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': f"{type(e).__name__}: {str(e)}"}, status=500)

            messages.error(request, f"{type(e).__name__}: {str(e)}")
            return redirect('product_list')

    @login_required(login_url='login')
    @staticmethod
    def delete_product(request, productid):
        try:
            product = get_object_or_404(Product, pk=productid)
            product.delete()

            # Check if the deletion request was initiated via asynchronous JS Fetch
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.method == 'POST':
                return JsonResponse({'success': True})

            messages.success(request, "Product deleted successfully.")

        except Exception as e:
            log_error(e)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': f"{type(e).__name__}: {str(e)}"}, status=500)
                
            messages.error(request, f"{type(e).__name__}: {str(e)}")

        return redirect('product_list')
    
    @login_required(login_url='login')
    @require_POST
    def bulk_delete_products(request):
        try:
            # Load string data array from request body input stream
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])

            if not product_ids:
                return JsonResponse({'success': False, 'error': 'No asset records targeted.'}, status=400)

            # Fire bulk filtration delete directly against SQL Server
            deleted_count, _ = Product.objects.filter(productid__in=product_ids).delete()

            return JsonResponse({
                'success': True,
                'message': f'Successfully cleared {deleted_count} tracks from core ledger rows.'
            })

        except Exception as e:
            # Log to your text file tool if available
            if 'log_error' in globals():
                log_error(e)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

'''FOR REGION'''

class Region_view:
    @login_required(login_url='login')
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

    @login_required(login_url='login')
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

    @login_required(login_url='login')
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

    @login_required(login_url='login')
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
    @login_required(login_url='login')
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

    @login_required(login_url='login')
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

    @login_required(login_url='login')
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

    @login_required(login_url='login')
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
@login_required(login_url='login')
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