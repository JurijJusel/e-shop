from rest_framework.generics import ListCreateAPIView
from .models import Hat
from .serializers import HatSerializer


class HatListCreateView(ListCreateAPIView):
    queryset = Hat.objects.all()
    serializer_class = HatSerializer


#from django.shortcuts import render

#def index(request):
#    return render(request, 'index.html')
