from django.urls import path
from .views import HatListCreateView, HatDetailView

urlpatterns = [
    path('hats/', HatListCreateView.as_view(), name='hat-list-create'),
    path('hats/<int:pk>/', HatDetailView.as_view(), name='hat-detail')
]
