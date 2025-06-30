from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image',
                  'image_url', 'images', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_name(self, value):
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Pavadinimas negali būti 'string' ar tuščias.")
        return value

    def validate_description(self, value):
        if not value:
            return "Aprašymas pagal nutylėjimą"
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Aprašymas negali būti 'string' ar tuščias.")
        return value

    def validate_price(self, value):
        if value < 1 or value > 1000:
            raise serializers.ValidationError("Kaina turi būti tarp 1 ir 1000.")
        return value
