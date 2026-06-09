from rest_framework import serializers
from .models import Product, Lead, Region


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product

        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"