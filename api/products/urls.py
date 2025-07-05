from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('all-products/', views.all_products_list, name='all-products'),
    path('products-by-price/', views.products_by_price, name='products-by-price'),
]
