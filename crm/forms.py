from django import forms
from .models import Product, Region


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'added_dts': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            )
        }


class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = '__all__'

        widgets = {
            'added_dts': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            )
        }