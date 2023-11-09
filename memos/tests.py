from django.test import TestCase

# Create your tests here.
# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {"user_name": "newuser", "email": "newuser@example.com", "password": "password123"}
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().user_name, 'newuser')
