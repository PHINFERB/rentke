from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id', 'title', 'price', 'address', 
                'property_type', 'bedrooms', 'bathrooms',
                'main_image']
        extra_kwargs = {'address': {'required': False}}
        read_only_fields = ('owner',)

    def get_main_image(self, obj):
        if obj.main_image:
            return self.context['request'].build_absolute_uri(obj.main_image.url)
        return None

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be positive")
        return super().validate(data)