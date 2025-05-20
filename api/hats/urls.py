from django.urls import path
from .views import (HatListCreateView, HatDetailView,
                    CartView, OrderListCreateView, OrderDetailView)


urlpatterns = [
    # Kepurių API
    path('hats/', HatListCreateView.as_view(), name='hat-list-create'),
    path('hats/<int:pk>/', HatDetailView.as_view(), name='hat-detail'),

    # Krepšelio API
    path('cart/', CartView.as_view(), name='cart-detail'),

    # Užsakymų API
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
