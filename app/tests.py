# pricing/tests.py
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
        
        # Create a pricing config
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
        # Test case 1: Within base distance, under 1 hour, no waiting
        data = {
            'distance': 2.5,
            'ride_time': 45,
            'waiting_time': 2,
            'date': '2023-06-01T12:00:00'  # Thursday
        }
        response = self.client.post('/api/calculate-price/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['price'], 80.0 + (45/60 * 1.0) + 0)
        
        # Test case 2: Beyond base distance, over 1 hour, with waiting
        data = {
            'distance': 4.0,
            'ride_time': 75,
            'waiting_time': 5,
            'date': '2023-06-03T12:00:00'  # Saturday
        }
        response = self.client.post('/api/calculate-price/', data, format='json')
        expected_price = (
            80.0 +  # DBP
            (1.0 * 30.0) +  # DAP for 1 extra km
            (75/60 * 1.25) +  # Time component
            (1 * 5.0)  # 1 block of waiting charges (5-3=2 mins, but we charge for whole block)
        )
        self.assertAlmostEqual(response.data['price'], expected_price)