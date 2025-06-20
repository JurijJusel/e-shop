from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet, CustomerViewSet,
                   CartViewSet, OrderViewSet, OrderStatusViewSet)


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-statuses', OrderStatusViewSet, basename='order-status')

urlpatterns = [
    path('', include(router.urls)),
]
