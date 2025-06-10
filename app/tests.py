from django.test import TestCase
from django.contrib.auth.models import User
from .models import PricingConfig
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

class PricingModuleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='admin', password='password')
        
        self.config = PricingConfig.objects.create(
            name="Test Config",
            is_active=True,
            dbp_amount=80.00,
            dbp_max_km=3.0,
            dbp_applicable_days="MON,TUE,WED,THU,FRI,SAT,SUN",
            dap_amount=30.00,
            tmf_under_1h=1.0,
            tmf_1h_to_2h=1.25,
            tmf_after_2h=2.2,
            wc_free_minutes=3,
            wc_amount_per_block=5.00,
            wc_block_duration=3
        )
    
    def test_price_calculation(self):
        data = {
            'distance': 2.5,
            'ride_time': 45,
            'waiting_time': 2,
            'date': '2023-06-01T12:00:00'
        }
        response = self.client.post('/api/calculate-price/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['price'], 80.0 + (45/60 * 1.0) + 0)
        
        data = {
            'distance': 4.0,
            'ride_time': 75,
            'waiting_time': 5,
            'date': '2023-06-03T12:00:00'
        }
        response = self.client.post('/api/calculate-price/', data, format='json')
        expected_price = (
            80.0 +
            (1.0 * 30.0) +
            (75/60 * 1.25) +
            (1 * 5.0)
        )
        self.assertAlmostEqual(response.data['price'], expected_price)