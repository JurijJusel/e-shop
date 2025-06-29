from rest_framework import serializers
from .models import Cart
from api.products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'products', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total']

    def get_total_price(self, obj):
        return obj.total_price()
