from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class User(AbstractUser):
    # Add any custom fields here
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
class Property(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE,
        related_name='properties',
        null=True,
        blank=True
    )
    class Meta:
        ordering = ['id']
    
    # Location
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, default="Nairobi")
    
    # Property Details
    property_type = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('land', 'Land'),
    ])
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    
    # Amenities
    has_parking = models.BooleanField(default=False)
    has_water = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=False)
    
    # Media
    main_image = models.ImageField(upload_to='property_images/')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - KSh {self.price}"
    def __str__(self):
        return f"{self.title} (Owned by: {self.owner.username})"

    class Meta:
        verbose_name_plural = "Properties"
