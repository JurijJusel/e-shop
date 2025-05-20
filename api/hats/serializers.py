from rest_framework import serializers
from .models import Hat, Customer, Cart, Order, OrderItem


class HatSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Hat
        fields = ['id', 'name', 'description', 'price', 'image', 'image_url', 'created_at', 'updated_at']

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
            return "Aprasymas pagal nutiliejima"
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
        fields = ['id', 'customer_id', 'phone', 'email', 'address']

class CartSerializer(serializers.ModelSerializer):
    hats = HatSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'hats', 'created_at', 'updated_at', 'total']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total']

    def get_total(self, obj):
        return sum(hat.price for hat in obj.hats.all())


class OrderItemSerializer(serializers.ModelSerializer):
    hat = HatSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'hat', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'shipping_address', 'order_date',
            'status', 'total_amount', 'payment_method',
            'payment_status', 'items'
        ]
        read_only_fields = ['id', 'customer', 'order_date', 'total_amount', 'items']
