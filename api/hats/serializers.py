from rest_framework import serializers
from .models import Hat
import random

class HatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hat
        fields = '__all__'  # ['id', 'name', 'price', 'description', 'image', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_name(self, value):
        if not value.strip():
            possible_names = [
                "geles", "spalvota", "gamtos spalvos",
                "ruduo", "pavasario spalvos", "saulė",
                "vėjas", "žiedas", "mėnulis", "žvaigždės"
            ]
            value = random.choice(possible_names)
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Pavadinimas negali būti 'string' ar tuščias.")
        return value

    def validate_description(self, value):
        if not value:
            return "Aprasymas pagal nutiliejima"
        if value.strip().lower() == 'string':
            raise serializers.ValidationError("Aprašymas negali būti 'string'")
        return value

    def validate_price(self, value):
        if value < 1 or value > 1000:
            raise serializers.ValidationError("Kaina turi būti tarp 1 ir 1000.")
        return value
