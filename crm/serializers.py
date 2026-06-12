from rest_framework import serializers
from .models import Product, Lead, Region
import re
from django.core.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):

    def validate_productname(self, value):
        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise serializers.ValidationError(
                "Only letters, numbers and spaces are allowed."
            )
        return value

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['productid', 'added_by', 'added_dts']

class RegionSerializer(serializers.ModelSerializer):

    def validate_regionname(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Only letters and spaces are allowed."
            )
        return value
    
    class Meta:
        model = Region
        fields = "__all__"
        read_only_fields = ['regionid', 'added_by', 'added_dts']

class LeadSerializer(serializers.ModelSerializer):

    def validate_personname(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Only letters and spaces are allowed.")
        return value

    def validate_companyname(self, value):
        if not re.match(r'^[A-Za-z0-9 &.-]+$', value):
            raise serializers.ValidationError("Invalid company name.")
        return value

    def validate_contactno(self, value):
        if not re.match(r'^[0-9]{10}$', value):
            raise serializers.ValidationError("Contact number must contain exactly 10 digits.")
        return value

    def validate_city(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Only letters and spaces are allowed.")
        return value

    def validate_state(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError("Only letters and spaces are allowed.")
        return value

    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ['leadid', 'added_by', 'added_dts']