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
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponse
from django.http import JsonResponse



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
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset
# def create view
def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)



# Basic Views
def home(request):
    return HttpResponse("API Working Properly")

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'admin': reverse('admin:index', request=request)
    })
