from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView, CreateAPIView,
                                    RetrieveAPIView,
                                    RetrieveUpdateDestroyAPIView,
                                    DestroyAPIView)
from .models import Hat, Customer, Cart, CartItem, Order, OrderItem
from .serializers import (HatSerializer, CartSerializer,
                        CartItemSerializer, OrderSerializer)


class HatListCreateView(ListCreateAPIView):
    queryset = Hat.objects.all()
    serializer_class = HatSerializer

class HatDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Hat.objects.all()
    serializer_class = HatSerializer

    def patch(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {"error": "PATCH užklausa turi turėti bent vieną lauką."},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super().patch(request, *args, **kwargs)
        hat = self.get_object()
        hat.updated_at = timezone.now()
        hat.save()
        return response


def get_or_create_customer(request, phone=None, email=None, address=None):

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
    else:
        if not phone or not email:
            raise ValueError("Phone and email are required for guest customers.")

        customer, _ = Customer.objects.get_or_create(
            phone=phone,
            email=email,
            defaults={'address': address}
        )
    return customer


class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hat = serializer.validated_data['hat']
        unit_price = hat.price
        phone = request.data.get('phone')
        email = request.data.get('email')
        address = request.data.get('address', '')

        if not phone or not email:
            return Response({"error": "Būtini laukai: phone ir email"}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_or_create_customer(request, phone, email, address)
        cart, _ = Cart.objects.get_or_create(customer=customer, is_active=True)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, hat=hat, defaults={'unit_price': unit_price}
        )

        if not created:
            cart_item.unit_price = unit_price
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class CartItemDeleteView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def delete(self, request, *args, **kwargs):
        try:
            cart_item = self.get_object()
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Prekė nesukuriama ar neberandama krepšelyje"}, status=status.HTTP_404_NOT_FOUND)


class CartView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        customer = get_or_create_customer(self.request)
        cart, _ = Cart.objects.get_or_create(customer=customer, is_active=True)
        return cart


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer = get_or_create_customer(self.request)
        return Order.objects.filter(customer=customer)

    def create(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        email = request.data.get("email")
        address = request.data.get("address", "")

        if not request.user.is_authenticated and (not phone or not email):
            return Response(
                {"error": "Svečias turi pateikti phone ir email"},
                status=status.HTTP_400_BAD_REQUEST
                )

        customer = get_or_create_customer(request, phone, email, address)
        cart = get_object_or_404(Cart, customer=customer, is_active=True)

        if not cart.items.exists():
            return Response({"error": "Krepšelis tuščias."}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.unit_price for item in cart.items.all())

        order = Order.objects.create(
            customer=customer,
            shipping_address=address,
            total_amount=total
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                hat=item.hat,
                unit_price=item.unit_price
            )

        cart.is_active = False
        cart.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
