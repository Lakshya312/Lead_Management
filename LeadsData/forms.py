from django import forms
from .models import Product, Region, Lead


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'ProductName',
            'Category',
            'Added_By'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Category'].empty_label = "---- select category ----"

    def clean_ProductName(self):
        try:
            product_name = self.cleaned_data.get('ProductName')

            if not product_name:
                raise forms.ValidationError("Product name required")

            if len(product_name) < 2:
                raise forms.ValidationError("Product name too short")

            return product_name

        except forms.ValidationError:
            raise


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = [
            'RegionName',
            'Added_By'
        ]

    def clean_RegionName(self):
        try:
            region_name = self.cleaned_data.get('RegionName')

            if not region_name:
                raise forms.ValidationError("Region name required")

            if len(region_name) < 2:
                raise forms.ValidationError("Region name too short")

            return region_name

        except forms.ValidationError:
            raise


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'PersonName',
            'Gender',
            'CompanyName',
            'ContactNo',
            'Email',
            'City',
            'State',
            'Territory',
            'Region',
            'Product',
            'Status',
            'Source',
            'BusinessNeed',
            'Added_By'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fk_fields = ['Product', 'Region', 'Territory', 'Status', 'Source']

        for f in fk_fields:
            self.fields[f].queryset = self.fields[f].queryset.order_by('pk')
            self.fields[f].empty_label = "----- select -----"
            self.fields[f].required = False

    def clean_PersonName(self):
        try:
            name = self.cleaned_data.get('PersonName')

            if not name:
                raise forms.ValidationError("Person name required")

            if len(name) < 2:
                raise forms.ValidationError("Enter valid name")

            return name

        except forms.ValidationError:
            raise

    def clean_ContactNo(self):
        try:
            contact = self.cleaned_data.get('ContactNo')

            if contact:
                if not contact.isdigit():
                    raise forms.ValidationError("Contact number only digits me hona chahiye")

                if len(contact) != 10:
                    raise forms.ValidationError("Contact number 10 digit ka hona chahiye")

            return contact

        except forms.ValidationError:
            raise

    def clean_Email(self):
        try:
            email = self.cleaned_data.get('Email')

            if email:
                if not email.endswith(".com"):
                    raise forms.ValidationError("Email .com se end hona chahiye")

            return email

        except forms.ValidationError:
            raise