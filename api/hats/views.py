from rest_framework.generics import ListCreateAPIView
from .models import Hat
from .serializers import HatSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status


class HatListCreateView(ListCreateAPIView):
    queryset = Hat.objects.all()
    serializer_class = HatSerializer

class HatDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Hat.objects.all()
    serializer_class = HatSerializer

    def patch(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {"error": "PATCH užklausa turi turėti bent vieną lauką."},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = super().patch(request, *args, **kwargs)
        hat = self.get_object()
        hat.updated_at = timezone.now()
        hat.save()
        return response
