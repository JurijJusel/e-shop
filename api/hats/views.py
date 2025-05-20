from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.generics import (ListCreateAPIView,
                                    RetrieveAPIView,
                                    RetrieveUpdateDestroyAPIView,
                                    RetrieveAPIView)
from .models import Hat, Customer, Cart, Order, OrderItem
from .serializers import (HatSerializer, CartSerializer, OrderSerializer)


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

    if not phone:
        phone = request.data.get('phone')
    if not email:
        email = request.data.get('email')
    if not address:
        address = request.data.get('address', '')

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


class CartView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        phone = self.request.query_params.get("phone")
        email = self.request.query_params.get("email")
        customer = get_or_create_customer(self.request, phone=phone, email=email)
        cart, created = Cart.objects.get_or_create(customer=customer)
        return cart

    def patch(self, request, *args, **kwargs):
        cart = self.get_object()
        hat_ids = request.data.get("hats", [])
        if not isinstance(hat_ids, list):
            return Response({"error": "Laukelyje 'hats' turi būti ID sąrašas."}, status=400)
        cart.hats.set(hat_ids)
        cart.save()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        phone = self.request.query_params.get("phone")
        email = self.request.query_params.get("email")
        customer = get_or_create_customer(self.request, phone=phone, email=email)
        return Order.objects.filter(customer=customer)

    def create(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        email = request.data.get("email")
        address = request.data.get("address", "")

        if not phone or not email:
            return Response({"error": "Būtini laukai: phone ir email"}, status=400)

        customer = get_or_create_customer(request, phone, email, address)
        cart = get_object_or_404(Cart, customer=customer)

        if not cart.hats.exists():
            return Response({"error": "Krepšelis tuščias."}, status=400)

        total = sum(hat.price for hat in cart.hats.all())

        order = Order.objects.create(
            customer=customer,
            shipping_address=address,
            total_amount=total
        )

        for hat in cart.hats.all():
            OrderItem.objects.create(
                order=order,
                hat=hat,
                unit_price=hat.price
            )

        cart.hats.clear()

        return Response(OrderSerializer(order).data, status=201)
