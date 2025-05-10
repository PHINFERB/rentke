from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate, APIClient
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.urls import reverse
from .models import Property
from .permissions import IsOwnerOrReadOnly
from .views import PropertyDetailView

class PropertyPaginationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.owner = User.objects.create_user(
            username='owner', 
            password='testpass123'
        )
        cls.non_owner = User.objects.create_user(
            username='nonowner', 
            password='testpass123'
        )
        cls.tester = User.objects.create_user(
            username='tester', 
            password='testpass123'
        )

        # Create test properties
        for i in range(25):
            Property.objects.create(
                title=f"Property {i+1}",
                price=100000 + (i * 5000),
                bedrooms=1 + (i % 3),
                bathrooms=1 + (i % 2),
                address=f"{i+100} Test Street",
                property_type=['apartment', 'house', 'studio'][i % 3],
                owner=cls.owner
            )

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.property = Property.objects.first()

    # Pagination Tests
    def test_pagination_defaults(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(reverse('property-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertEqual(response.data['count'], 25)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_custom_page_size(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(reverse('property-list'), {'page_size': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_page_navigation(self):
        self.client.force_authenticate(user=self.owner)
        # First page
        page1 = self.client.get(reverse('property-list'), {'page': 1, 'page_size': 5})
        # Second page
        page2 = self.client.get(reverse('property-list'), {'page': 2, 'page_size': 5})
        
        self.assertNotEqual(
            page1.data['results'][0]['id'],
            page2.data['results'][0]['id']
        )

    def test_max_page_size(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(reverse('property-list'), {'page_size': 150})
        self.assertEqual(len(response.data['results']), 100)  # Max page size

    # Permission Tests
    def test_owner_has_full_access(self):
        request = self.factory.get('/fake-url/')
        request.user = self.owner
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )
        
        request = self.factory.put('/fake-url/')
        request.user = self.owner
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )
        
        request = self.factory.delete('/fake-url/')
        request.user = self.owner
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )

    def test_non_owner_read_only(self):
        request = self.factory.get('/fake-url/')
        request.user = self.non_owner
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )
        
        request = self.factory.put('/fake-url/')
        request.user = self.non_owner
        self.assertFalse(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )

    def test_unauthenticated_read_only(self):
        request = self.factory.get('/fake-url/')
        request.user = None
        self.assertTrue(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )
        
        request = self.factory.post('/fake-url/')
        request.user = None
        self.assertFalse(
            IsOwnerOrReadOnly().has_object_permission(
                request, 
                None, 
                self.property
            )
        )

    def test_permission_in_view(self):
        complete_data = {
            'title': 'Updated Property',
            'price': 1500,
            'address': '123 New Street',
            'property_type': 'house',
            'bedrooms': 2,
            'bathrooms': 1
        }

        # Test GET (read) allowed for anyone
        request = self.factory.get(f'/properties/{self.property.id}/')
        response = PropertyDetailView.as_view()(request, pk=self.property.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test PUT (write) denied for non-owner
        request = self.factory.put(
            f'/properties/{self.property.id}/',
            data=complete_data,
            content_type='application/json'
        )
        force_authenticate(request, user=self.non_owner)
        response = PropertyDetailView.as_view()(request, pk=self.property.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test PUT allowed for owner
        request = self.factory.put(
            f'/properties/{self.property.id}/',
            data=complete_data,
            content_type='application/json'
        )
        force_authenticate(request, user=self.owner)
        response = PropertyDetailView.as_view()(request, pk=self.property.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)