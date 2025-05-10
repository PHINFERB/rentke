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
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
    
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]


def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        return queryset

def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Property List and Create View
class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]

from django.http import HttpResponse

# Basic Views
def home(request):
    return HttpResponse("API Working Properly")

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'properties': reverse('property-list', request=request, format=format),
        'admin': reverse('admin:index', request=request)
    })