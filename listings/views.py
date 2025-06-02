from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Property
from rest_framework import viewsets
from .serializers import PropertySerializer
from .pagination import PropertyPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.generics import ListAPIView

class UserPropertiesView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination
    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)
# Search properties view
class SearchPropertiesView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination

    def get_queryset(self):
        queryset = Property.objects.all()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        return queryset
# Welcome view for Rentke API
def rentke_view(request):
    return HttpResponse("WELCOME TO RENTKE API.")
# Traditional Django view
def my_view(request):
    properties = Property.objects.all()
    return render(request, 'listings/property_list.html',
                 {'properties': properties})

# DRF API Views Property views
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('id')
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly]
    
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PropertyPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# API view for listings
def listings_api(request):
    data = {
        "message": "You are the best",
        "listings": [
            {"id": 1, "title": "Sample Listing 1"},
            {"id": 2, "title": "Sample Listing 2"}
        ]
    }
    return JsonResponse(data)

# Property List and Create View
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]

class PublicPropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    permission_classes = []

    def get_queryset(self):
        return Property.objects.filter(is_public=True).order_by('-created_at')



# Basic Views
def home(request):
    return HttpResponse("API Working Properly")

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'admin': reverse('admin:index', request=request)
    })
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'user-properties': reverse('user-properties', request=request, format=format),
        'search': reverse('property-search', request=request, format=format),
        'public-listings': reverse('public-listings', request=request, format=format),
        'admin': reverse('admin:index', request=request)
    })