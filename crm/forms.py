from django import forms
from .models import *
import re
from django.core.exceptions import ValidationError


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
            'productname': forms.TextInput(attrs={
            'pattern': '[A-Za-z0-9 ]+$',
            'title': 'Only letters, numbers and spaces are allowed.'
        }),
            # Enforces a strict dropdown configuration with an empty selection placeholder
            'is_active': forms.Select(choices=[
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

        widgets = {
            'regionname': forms.TextInput(attrs={
            'pattern': '^[A-Za-z ]+$',
            'title': 'Only letters and spaces are allowed.'
            })
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
            'personname': forms.TextInput(attrs={
            'pattern': '^[A-Za-z ]+$',
            'title': 'Only letters and spaces are allowed.'
        }),
            'gender': forms.TextInput(attrs={
            'pattern': '^(Male|Female|Other)$',
            'title': 'Enter Male, Female or Other.'
        }),

            'companyname': forms.TextInput(attrs={
            'pattern': '^[A-Za-z0-9 &.-]+$',
            'title': 'Only letters, numbers, spaces, &, . and - are allowed.'
        }),

            'contactno': forms.TextInput(attrs={
            'pattern': '^[0-9]{10}$',
            'title': 'Enter exactly 10 digits.'
        }),

            'email': forms.EmailInput(attrs={
            'type': 'email',
            'title': 'Enter a valid email address.'
        }),

            'city': forms.TextInput(attrs={
            'pattern': '^[A-Za-z ]+$',
            'title': 'Only letters and spaces are allowed.'
        }),

            'state': forms.TextInput(attrs={
            'pattern': '^[A-Za-z ]+$',
            'title': 'Only letters and spaces are allowed.'
        }),

            'executiveid': forms.NumberInput(attrs={
            'min': '1',
            'step': '1',
            'title': 'Enter a positive integer.'
        }),
            # Fixed to type="date" to match the DateField model configuration
            'lead_gen_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'premium-cyber-input-element'
                    },
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