from django import forms
from django.db.models import Q
from .models import Region, Product, Lead

class RegionForm(forms.ModelForm):
    """
    RegionForm with a dynamic dropdown for regionname.
    Choices are fetched from the database (tbl_region_master) at form
    instantiation time — no hardcoded values anywhere.
    """
    regionname = forms.ChoiceField(
        choices=[],  # populated dynamically in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Region Name',
    )

    class Meta:
        model = Region
        fields = ['regionname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pull all existing region names from DB at runtime
        db_choices = [('', '-- Select Region Name --')] + [
            (r.regionname, r.regionname)
            for r in Region.objects.all().order_by('regionname')
        ]
        self.fields['regionname'].choices = db_choices

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['productname', 'categoryid', 'is_active']
        labels = {
            'productname': 'Product Name',
            'categoryid': 'Category',
            'is_active': 'Status',
        }
        widgets = {
            'productname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Product Name (e.g. Laptop Pro, 3M Tape)',
            }),
            'categoryid': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(1, 'Active'), (0, 'Inactive')]
            ),
        }

    def clean_productname(self):
        """
        Validate that the product name is NOT purely numeric.
        Pure integers like '1234' or '007' are rejected.
        Alphanumeric names like 'Product2', '3M Tape', 'A1B2' are accepted.
        """
        name = self.cleaned_data.get('productname', '').strip()
        if not name:
            raise forms.ValidationError("Product name is required.")
        # Strip spaces and check if everything left is a digit
        if name.replace(' ', '').isdigit():
            raise forms.ValidationError(
                "Product name cannot be purely numeric. "
                "Please include at least one letter (e.g. \"Product 101\" or \"3M Cable\")."
            )
        return name

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'personname', 'gender', 'companyname', 'contactno', 'email',
            'city', 'state', 'territoryid', 'regionid', 'productid',
            'statusid', 'leadsourceid', 'businessneed', 'executiveid'
        ]
        labels = {
            'personname': 'Person Name',
            'gender': 'Gender',
            'companyname': 'Company Name',
            'contactno': 'Contact No',
            'email': 'Email',
            'city': 'City',
            'state': 'State',
            'territoryid': 'Territory',
            'regionid': 'Region',
            'productid': 'Product',
            'statusid': 'Lead Status',
            'leadsourceid': 'Lead Source',
            'businessneed': 'Business Need',
            'executiveid': 'Executive ID',
        }
        widgets = {
            'personname': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[('', '-- Select Gender --'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'companyname': forms.TextInput(attrs={'class': 'form-control'}),
            'contactno': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'numeric', 'pattern': '[0-9]*', 'title': 'Please enter numbers only'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'territoryid': forms.Select(attrs={'class': 'form-select'}),
            'regionid': forms.Select(attrs={'class': 'form-select'}),
            'productid': forms.Select(attrs={'class': 'form-select'}),
            'statusid': forms.Select(attrs={'class': 'form-select'}),
            'leadsourceid': forms.Select(attrs={'class': 'form-select'}),
            'businessneed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'executiveid': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'numeric', 'pattern': '[0-9]*', 'title': 'Please enter integer numbers only'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        contactno = cleaned_data.get("contactno")

        if email or contactno:
            query = Q()
            if email:
                query |= Q(email=email)
            if contactno:
                query |= Q(contactno=contactno)
            
            duplicate_leads = Lead.objects.filter(query)
            if self.instance and self.instance.pk:
                duplicate_leads = duplicate_leads.exclude(pk=self.instance.pk)
                
            if duplicate_leads.exists():
                raise forms.ValidationError("A lead with this Email or Contact Number already exists.")
                
        return cleaned_data
