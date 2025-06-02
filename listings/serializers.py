from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    is_owner = serializers.SerializerMethodField()
    main_image_url = serializers.SerializerMethodField()
    main_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Property
        fields = [
            'id', 
            'title',
            'description',
            'price',
            'address',
            'city',
            'property_type',
            'bedrooms',
            'bathrooms',
            'has_parking',
            'has_water',
            'has_wifi',
            'main_image',  # The actual ImageField
            'main_image_url',  # URL for the main image
            'owner',
            'is_owner',
            'is_public',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_main_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.main_image.url) if request else obj.main_image.url
        return None

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request else False

    def validate(self, data):
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be positive")
        return data