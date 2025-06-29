from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_id', 'phone', 'email', 'address',
                  'created_at', 'updated_at']
