from rest_framework import serializers
from .models import Product,Region,Lead
import re

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},
        }

    def validate_ProductName(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Product Name Can Only Contain Alphabets"
            )
        return value
    
class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"

        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},
        }
        
    def validate_RegionName(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Region Name Can Only Contain Alphabets"
            )
        return value

    
class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = "__all__"

        extra_kwargs = {
            'Added_By': {'required': False},
            'Added_Dts': {'required': False},
        }
        
    def validate_LeadName(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Lead Name Can Only Contain Alphabets"
            )
        return value

    def validate_PhoneNo(self, value):
        if not re.match(r'^[6-9]\d{9}$', str(value)):
            raise serializers.ValidationError(
                "Please Enter Valid Phone Number"
            )
        return value
    
    def validate_EmailId(self, value):
        if not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', value):
            raise serializers.ValidationError(
                "Please Enter Valid Email Address"
            )
        return value
    
    def validate_CompanyName(self, value):
        if not re.match(r'^[A-Za-z ]+$', value):
            raise serializers.ValidationError(
                "Company Name Can Only Contain Alphabets"
            )
        return value

