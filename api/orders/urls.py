from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderStatusViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'statuses', OrderStatusViewSet, basename='statuses')

urlpatterns = [
    path('', include(router.urls)),
]
