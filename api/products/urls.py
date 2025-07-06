from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')


urlpatterns = [
    path('products/all/', views.AllProductsList.as_view(), name='all-products'),
    path('products/price/', views.ProductsByPrice.as_view(), name='products-by-price'),
    path('', include(router.urls)),
]
