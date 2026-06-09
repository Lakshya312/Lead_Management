from django import forms
from .models import *


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['productname', 'categoryid', 'is_active']

        labels = {
            'productname': 'Product Name',
            'categoryid': 'Category Name',
            'is_active': 'Is Active Status',
        }

        widgets = {
            # Enforces a strict dropdown configuration with an empty selection placeholder
            'is_active': forms.Select(choices=[
                ('', '--- Select Status ---'),
                ('1', 'Active'),
                ('0', 'Inactive')
            ]),
            
            'added_dts': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    # Injecting placeholders dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sets the first/default unselected option text
        self.fields['categoryid'].empty_label = "--- Select Category ---"

class RegionForm(forms.ModelForm):

    # 1. Define the strict list of allowed geographic permutations
    REGION_CHOICES = [
        ('', '--- Select Region ---'),  # Default placeholder
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
        ('North-East', 'North-East'),
        ('North-West', 'North-West'),
        ('South-East', 'South-East'),
        ('South-West', 'South-West'),
        ('Central', 'Central'),
    ]

    # 2. Override the form field to render as a Select Choice Dropdown
    regionname = forms.ChoiceField(
        choices=REGION_CHOICES,
        label='Region Name',
        widget=forms.Select()
    )

    class Meta:
        model = Region

        fields = [
            'regionname'
        ]

        labels = {
            'regionname': 'Region Name',
        }

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'personname', 'gender', 'companyname', 'contactno', 'email',
            'city', 'state', 'territoryid', 'regionid', 'productid',
            'statusid', 'leadsourceid', 'businessneed', 'lead_gen_date', 'executiveid'
        ]

        labels = {
            'personname': 'Person Name',
            'gender': 'Gender',
            'companyname': 'Company Name',
            'contactno': 'Contact Number',
            'email': 'Email Address',
            'city': 'City',
            'state': 'State',
            'territoryid': 'Territory',
            'regionid': 'Region',
            'productid': 'Product Selection',
            'statusid': 'Lead Status',
            'leadsourceid': 'Lead Source',
            'businessneed': 'Business Need Description',
            'lead_gen_date': 'Lead Generation Date',
            'executiveid': 'Executive ID Number'
        }

        widgets = {
            # Fixed to type="date" to match the DateField model configuration
            'lead_gen_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'businessneed': forms.Textarea(attrs={'rows': 3}),
        }
        
    # Injecting placeholders dynamically for all Foreign Key dropdowns
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['territoryid'].empty_label = "--- Select Territory ---"
        self.fields['regionid'].empty_label = "--- Select Region ---"
        self.fields['productid'].empty_label = "--- Select Product ---"
        self.fields['statusid'].empty_label = "--- Select Status ---"
        self.fields['leadsourceid'].empty_label = "--- Select Lead Source ---"