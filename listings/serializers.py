from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Show owner username
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'price', 'address', 
            'city', 'property_type', 'bedrooms', 
            'bathrooms', 'has_parking', 'has_water',
            'has_wifi', 'main_image_url', 'owner'
        ]
        extra_kwargs = {
            'address': {'required': False},
            'owner': {'read_only': True}
        }

    def validate(self, data):
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be positive")
        return data