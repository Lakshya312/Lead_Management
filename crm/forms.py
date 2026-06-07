from django import forms
from .models import Product


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