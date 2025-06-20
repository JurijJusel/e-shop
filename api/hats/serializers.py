from rest_framework import serializers
from .models import Product, ProductImage, Customer, Cart, Order, OrderStatus


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image',
                  'image_url', 'images', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_name(self, value):
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Pavadinimas negali būti 'string' ar tuščias.")
        return value

    def validate_description(self, value):
        if not value:
            return "Aprašymas pagal nutylėjimą"
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Aprašymas negali būti 'string' ar tuščias.")
        return value

    def validate_price(self, value):
        if value < 1 or value > 1000:
            raise serializers.ValidationError("Kaina turi būti tarp 1 ir 1000.")
        return value


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_id', 'phone', 'email', 'address',
                  'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'products', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total']

    def get_total_price(self, obj):
        return obj.total_price()


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'cart', 'customer', 'amount_paid', 'created_at', 'updated_at']


class OrderStatusSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderStatus
        fields = ['id', 'order', 'delivery_status', 'order_status',
                  'payment_status', 'created_at', 'updated_at']
