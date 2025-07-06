from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'price': ['lte', 'gte', 'exact'],
    }
    search_fields = ['name','description']


class AllProductsList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductsByPrice(APIView):
    def get(self, request, max_price=None):
        products = Product.objects.all()
        if max_price:
            try:
                max_price_decimal = Decimal(max_price)
                products = products.filter(price__lte=max_price_decimal)
            except (ValueError, TypeError):
                return Response({"error": "Invalid price format"}, status=400)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
