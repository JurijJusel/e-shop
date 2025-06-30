from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderStatusSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('cart', 'customer').all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'cart']

class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.select_related('order').all()
    serializer_class = OrderStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'order_status', 'payment_status']
