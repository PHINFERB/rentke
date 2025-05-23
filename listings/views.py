from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Property
from .serializers import PropertySerializer
from .pagination import PropertyPagination
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

# Basic views
def rentke_view(request):
    """Welcome view for Rentke backend"""
    return HttpResponse("WELCOME TO RENTKE BACK END")

def home(request):
    """API health check view"""
    return HttpResponse("API WORKING PROPERLY")

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """API entry point with endpoint links"""
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'public-listings': reverse('public-listings', request=request, format=format),
        'admin': reverse('admin:index', request=request)
    })

# Property Views
class PropertyViewSet(viewsets.ModelViewSet):
    """
    Viewset for property CRUD operations
    Requires authentication for write operations
    """
    queryset = Property.objects.all().order_by('id')
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Optionally filter by city if provided in query params"""
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a property"""
        serializer.save(owner=self.request.user)

# Public API Views
class PublicPropertyListView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'city', 'bedrooms']
    pagination_class = PropertyPagination
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    queryset = Property.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
         # Get the paginated response
        response = super().list(request, *args, **kwargs)
        """Custom list response with additional message"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Public listings retrieved successfully",
            "listings": serializer.data,
            "count": queryset.count()
        })

# Traditional Django views
def property_list_view(request):
    """Traditional Django template view for property listings"""
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'listings/property_list.html',
                {'properties': properties})