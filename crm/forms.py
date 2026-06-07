from django import forms
from .models import *


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'productname',
            'categoryid',
            'is_active'
        ]

        widgets = {
            'added_dts': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region

        fields = [
            'regionname'
        ]

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'personname', 'gender', 'companyname', 'contactno', 'email',
            'city', 'state', 'territoryid', 'regionid', 'productid',
            'statusid', 'leadsourceid', 'businessneed', 'lead_gen_date', 'executiveid'
        ]
        widgets = {
            # Fixed to type="date" to match the DateField model configuration
            'lead_gen_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'businessneed': forms.Textarea(attrs={'rows': 3}),
        }