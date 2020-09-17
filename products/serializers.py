from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)

    class Meta:
        model = Product
        fields = ('product_id', 'name', 'description', 'price',
                  'is_on_sale', 'current_price')
