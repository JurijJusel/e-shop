from django.urls import path
from .views import HatListCreateView

urlpatterns = [
    path('hats/', HatListCreateView.as_view(), name='hat-list-create'),
]
