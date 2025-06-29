from rest_framework import serializers
from .models import Order, OrderStatus
from api.carts.serializers import CartSerializer
from api.customers.serializers import CustomerSerializer
from api.carts.models import Cart
from api.customers.models import Customer


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), source='cart', write_only=True, required=False
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'cart', 'cart_id', 'customer', 'customer_id', 'amount_paid', 'created_at', 'updated_at']

    def validate(self, data):
        cart = data.get('cart')
        amount_paid = data.get('amount_paid', 0)
        if cart and amount_paid != cart.total_price():
            raise serializers.ValidationError("Amount paid must match the cart's total price.")
        return data


class OrderStatusSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = OrderStatus
        fields = ['id', 'order', 'order_id', 'delivery_status', 'order_status', 'payment_status', 'created_at', 'updated_at']

    def validate_delivery_status(self, value):
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError("Delivery status must be at least 3 characters long if provided.")
        return value

    def validate(self, data):
        order_status = data.get('order_status')
        payment_status = data.get('payment_status')
        if order_status == 'delivered' and payment_status == 'unpaid':
            raise serializers.ValidationError("Order cannot be delivered if payment is unpaid.")
        return data
