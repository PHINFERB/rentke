from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'price', 'address', 'property_type', 'bedrooms', 'bathrooms'] 
        extr_kwargs = {'address': {'required': False}}
    read_only_fields = ('owner',)

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be positive")
        return data