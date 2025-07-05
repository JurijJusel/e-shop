from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'price': ['lte', 'gte', 'exact'],
    }
    search_fields = ['name','description']


@api_view(['GET'])
def all_products_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def products_by_price(request):
    max_price = request.query_params.get('price')
    products = Product.objects.all()
    if max_price:
        try:
            products = products.filter(price__lte=max_price)
        except (ValueError, TypeError):
            return Response({"error": "Invalid price format"}, status=400)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
