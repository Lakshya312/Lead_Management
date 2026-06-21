from django import forms
from .models import Product, Region ,Lead
import re
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    def clean_ProductID(self):

        product_id = self.cleaned_data.get(
        "ProductID"
    )

        if product_id <= 0:
            raise ValidationError(
            "Product ID must be greater than 0."
        )

        return product_id
    
    def clean_ProductName(self):

        product_name = self.cleaned_data.get(
        "ProductName"
    )

        if not re.match(
            r'^[A-Za-z\s]+$',
            product_name
        ):
            raise forms.ValidationError(
            "Product Name can contain only alphabets and spaces."
        )

        return product_name

    class Meta:
        model = Product
        exclude = ["Added_By", "Added_Dts"]
        widgets = {
            "ProductID": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "ProductName": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "CategoryID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "Is_Active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

class RegionForm(forms.ModelForm):
    def clean_RegionID(self):

        region_id = self.cleaned_data.get(
        "RegionID"
    )

        if region_id <= 0:
            raise ValidationError(
            "Region ID must be greater than 0."
        )

        return region_id
    
    class Meta:
        model = Region
        exclude = ["Added_By", "Added_Dts"]
        widgets = {
            "RegionID": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "RegionName": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

class LeadForm(forms.ModelForm):
    def clean_LeadID(self):

        lead_id = self.cleaned_data.get("LeadID")

        if lead_id <= 0:
            raise forms.ValidationError(
                "Lead ID must be greater than 0."
        )

        return lead_id
    def clean_PersonName(self):

        person_name = self.cleaned_data.get("PersonName")

        if not re.match(
            r'^[A-Za-z\s]+$',
            person_name
        ):
            raise forms.ValidationError(
                "Person Name can contain only alphabets and spaces."
            )

        return person_name
    def clean_ContactNo(self):

        contact_no = self.cleaned_data.get("ContactNo")

        if not re.match(
            r'^[0-9]{10}$',
            contact_no
        ):
            raise forms.ValidationError(
                "Contact Number must be 10 digits."
            )

        return contact_no
    def clean_BusinessNeed(self):

        business_need = self.cleaned_data.get("BusinessNeed")

        if len(business_need) < 10:
            raise forms.ValidationError(
                "Business Need must be at least 10 characters."
            )

        return business_need
    def clean_Email(self):

        email = self.cleaned_data.get("Email")

        if not re.fullmatch(
        r"[a-zA-Z0-9._%+-]+@gmail\.com",
            email
        ):
            raise forms.ValidationError(
            "Only Gmail addresses are allowed."
        )

        return email
    def clean_CompanyName(self):

        company_name = self.cleaned_data.get("CompanyName")

        if not re.match(
            r'^[A-Za-z\s]+$',
            company_name
        ):
            raise forms.ValidationError(
                "Company Name can contain only alphabets and spaces."
            )

        return company_name
    def clean_City(self):

        city = self.cleaned_data.get("City")

        if not re.fullmatch(r"[A-Za-z ]+", city):
            raise forms.ValidationError(
            "City can contain only alphabets."
        )

        return city
    def clean_State(self):

        state = self.cleaned_data.get("State")

        if not re.fullmatch(r"[A-Za-z ]+", state):
            raise forms.ValidationError(
            "State can contain only alphabets."
        )

        return state
    class Meta:
        model = Lead
        exclude = ["Added_By", "Added_Dts"]
        labels = {
            "TerritoryID": "Territory",
            "RegionID": "Region",
            "ProductID": "Product",
            "StatusID": "Status",
            "LeadSourceID": "Lead Source",
            "Lead_Gen_Date": "Lead Generated Date",
            "ExecutiveID": "Executive"
        }

        widgets = {
            "LeadID": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "PersonName": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "Gender": forms.Select(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female")
                ],
                attrs={"class": "form-select"}
            ),
            "CompanyName": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "ContactNo": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "Email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "City": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "State": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "RegionID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "TerritoryID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "ProductID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "StatusID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "LeadSourceID": forms.Select(
                attrs={"class": "form-select"}
            ),
            "BusinessNeed": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
            "Lead_Gen_Date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "ExecutiveID": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }