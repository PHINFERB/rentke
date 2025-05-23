from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse

# Constants at module level (shared across models)
PROPERTY_TYPES = [
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('studio', 'Studio'),
    ('land', 'Land'),
]

class Property(models.Model):
    """Main property listing model"""
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='properties',
        null=True,
        blank=True
    )
    # Location
    address = models.CharField(max_length=255, blank=True, null=True, default="",  # Default to empty string
    help_text="Street address of the property")
    city = models.CharField(max_length=100, default="Nairobi")
    
    # Property Details
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    
    # Amenities
    has_parking = models.BooleanField(default=False)
    has_water = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=False)
    
    # Main Image
    main_image = models.ImageField(
        upload_to='property_images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Primary display image"
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.owner:
            return f"{self.title} (Owned by: {self.owner.username})"
        return f"{self.title} - KSh {self.price}"
    
    def get_absolute_url(self):
        return reverse('property-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Properties"


class PropertyImage(models.Model):
    """Additional images for a property"""
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='additional_images'
    )
    image = models.ImageField(
        upload_to='property_images/%Y/%m/%d/',
        help_text="Additional property images"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Sorting order"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Property Images"

    def __str__(self):
        return f"Image #{self.order} for {self.property.title}"