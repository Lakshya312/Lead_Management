from rest_framework import serializers
from .models import Product, Lead, Region
import re


class ProductSerializer(serializers.ModelSerializer):

    def validate_productname(self, value):

        if not value:
            raise serializers.ValidationError(
                "Product Name is required."
            )

        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise serializers.ValidationError(
                "Only letters, numbers and spaces are allowed."
            )

        if Product.objects.filter(productname=value).exists():
            raise serializers.ValidationError(
                "Product with this name already exists."
            )

        return value

    def validate_categoryid(self, value):
        if value is None:
            raise serializers.ValidationError(
                "Category is required."
            )
        return value

    class Meta:
        model = Product
        fields = '__all__'

        read_only_fields = [
            'productid',
            'added_by',
            'added_dts'
        ]

        extra_kwargs = {
            'categoryid': {
                'required': True
            }
        }

class RegionSerializer(serializers.ModelSerializer):

    def validate_regionname(self, value):
        if not value:
            raise serializers.ValidationError(
                "Region Name is required."
            )

        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Only letters and spaces are allowed."
            )

        if Region.objects.filter(regionname=value).exists():
            raise serializers.ValidationError(
                "Region with this name already exists."
            )

        return value
    
    class Meta:
        model = Region
        fields = "__all__"
        read_only_fields = ['regionid', 'added_by', 'added_dts']

class LeadSerializer(serializers.ModelSerializer):

    def validate_personname(self, value):
        if not value:
            raise serializers.ValidationError(
                "Person Name is required."
            )

        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise serializers.ValidationError(
                "Only letters, numbers and spaces are allowed."
            )

        if Lead.objects.filter(personname=value).exists():
            raise serializers.ValidationError(
                "Lead with this name already exists. Add another name or use a different user name."
            )

        return value

    def validate_gender(self, value):
        if not value:
            raise serializers.ValidationError(
                "Gender is required."
            )

        if value not in ["Male", "Female", "Other"]:
            raise serializers.ValidationError(
                "Gender must be Male, Female or Other."
            )

        return value

    def validate_companyname(self, value):
        if not value:
            raise serializers.ValidationError(
                "Company Name is required."
            )

        if not re.match(r'^[A-Za-z0-9 &.-]+$', value):
            raise serializers.ValidationError(
                "Invalid company name."
            )

        return value

    def validate_contactno(self, value):
        if not value:
            raise serializers.ValidationError(
                "Contact Number is required."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Contact number must contain exactly 10 digits."
            )

        if not re.match(r'^[0-9]{10}$', value):
            raise serializers.ValidationError(
                "Contact number must contain only digits."
            )

        if Lead.objects.filter(contactno=value).exists():
            raise serializers.ValidationError(
                "Lead with this contact number already exists."
            )

        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(
                "Email is required."
            )

        if Lead.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Lead with this email already exists."
            )

        return value

    def validate_city(self, value):
        if not value:
            raise serializers.ValidationError(
                "City is required."
            )

        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Only letters and spaces are allowed."
            )

        return value

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError(
                "State is required."
            )

        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Only letters and spaces are allowed."
            )

        return value

    def validate_businessneed(self, value):
        if not value:
            raise serializers.ValidationError(
                "Business Need is required."
            )
        return value

    class Meta:
        model = Lead
        fields = "__all__"

        read_only_fields = [
            'leadid',
            'added_by',
            'added_dts'
        ]

        extra_kwargs = {
            'personname': {'required': True},
            'gender': {'required': True},
            'companyname': {'required': True},
            'contactno': {'required': True},
            'email': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'territoryid': {'required': True},
            'regionid': {'required': True},
            'productid': {'required': True},
            'statusid': {'required': True},
            'leadsourceid': {'required': True},
            'businessneed': {'required': True},
            'lead_gen_date': {'required': True},
            'executiveid': {'required': True},
        }