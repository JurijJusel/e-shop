from rest_framework import serializers
from .models import Hat


class HatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hat
        fields = '__all__'  # ['id', 'name', 'price', 'description', 'image', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
