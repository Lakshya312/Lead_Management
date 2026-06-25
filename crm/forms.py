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
            'title': 'Only letters, numbers and spaces are allowed.',
            'required':True,
            'id':'productname'
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
            ),
            'categoryid': forms.Select(attrs={'required':True})
        }

    # Injecting placeholders dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sets the first/default unselected option text
        self.fields['categoryid'].empty_label = "--- Select Category ---"

class RegionForm(forms.ModelForm):

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
<<<<<<< HEAD
            'pattern': '^[A-Za-z ]+$',
=======
            'pattern': '^[A-Za-z -]+$',
>>>>>>> lakshya-dev
            'title': 'Only letters and spaces are allowed.',
            'required':True,
            'id':'regionname'
            })
        }

    def clean_regionname(self):
        value = self.cleaned_data['regionname']

        if Region.objects.filter(regionname=value).exists():
            raise forms.ValidationError(
                "Region with this name already exists."
            )

        return value

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
                'pattern': '^[A-Za-z0-9 ]+$',
                'title': 'Only letters, numbers and spaces are allowed.',
                'required':True,
                'id':'personname'
            }),

            'gender': forms.Select(choices=[
                ('', '--- Select Gender ---'),
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other')
            ],
            attrs={
                'required':True
            }),

            'companyname': forms.TextInput(attrs={
                'pattern': '^[A-Za-z0-9 &.-]+$',
                'title': 'Invalid company name.',
                'required':True
            }),

            'contactno': forms.TextInput(attrs={
                'pattern': '^[0-9]{10}$',
                'maxlength': '10',
                'title': 'Enter exactly 10 digits.',
                'maxlength':10,
                'required':True,
                'id':'contactno'
            }),

            'email': forms.EmailInput(attrs={
                'required':True,
                'id':'email'
            }),

            'city': forms.TextInput(attrs={
                'pattern': '^[A-Za-z ]+$',
                'title': 'Only letters and spaces are allowed.',
                'required':True
            }),

            'state': forms.TextInput(attrs={
                'pattern': '^[A-Za-z ]+$',
                'title': 'Only letters and spaces are allowed.',
                'required':True
            }),

            'executiveid': forms.NumberInput(attrs={
                'min': '1',
                'required':True
            }),

            'lead_gen_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'required':True},
                format='%Y-%m-%d',
            ),

            'businessneed': forms.Textarea(attrs={
                'rows': 3,
                'required':True
            }),
        }
        
    # Injecting placeholders dynamically for all Foreign Key dropdowns
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['territoryid'].empty_label = "--- Select Territory ---"
        self.fields['regionid'].empty_label = "--- Select Region ---"
        self.fields['productid'].empty_label = "--- Select Product ---"
        self.fields['statusid'].empty_label = "--- Select Status ---"
        self.fields['leadsourceid'].empty_label = "--- Select Lead Source ---"

    def clean_personname(self):
<<<<<<< HEAD
        value = self.cleaned_data['personname']

        if Lead.objects.filter(personname=value).exists():
=======

        value = self.cleaned_data['personname']

        qs = Lead.objects.filter(
            personname=value
        )

        if self.instance.pk:
            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():
>>>>>>> lakshya-dev
            raise forms.ValidationError(
                "Lead with this name already exists. Add another name."
            )

        return value


    def clean_contactno(self):
<<<<<<< HEAD
        value = self.cleaned_data['contactno']

        if Lead.objects.filter(contactno=value).exists():
=======

        value = self.cleaned_data['contactno']

        qs = Lead.objects.filter(
            contactno=value
        )

        if self.instance.pk:
            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():
>>>>>>> lakshya-dev
            raise forms.ValidationError(
                "Lead with this contact number already exists."
            )

        return value


    def clean_email(self):
<<<<<<< HEAD
        value = self.cleaned_data['email']

        if Lead.objects.filter(email=value).exists():
=======

        value = self.cleaned_data['email']

        qs = Lead.objects.filter(
            email=value
        )

        if self.instance.pk:
            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():
>>>>>>> lakshya-dev
            raise forms.ValidationError(
                "Lead with this email already exists."
            )

        return value