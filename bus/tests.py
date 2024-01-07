# File: myapp/tests.py (replace 'myapp' with the actual name of your Django app)

from django.test import TestCase
from django.utils import timezone
from .models import Provider, BusStop, Bus, BusRoute, Notification

class ModelTests(TestCase):

    def setUp(self):
        # Create test data for models
        self.provider = Provider.objects.create(name="Test Provider", description="Test Provider Description")
        self.bus_stop = BusStop.objects.create(stop_point=12345, common_name="Test Bus Stop")
        self.bus = Bus.objects.create(bus_id="TEST001")
        self.bus_route = BusRoute.objects.create(
            arrival_time=timezone.now(),
            bus_id="TEST001",
            stop_point=12345,
            common_name="Test Bus Stop"
        )
        self.notification = Notification.objects.create(title="Test Notification", description="Test Notification Description")

    def test_provider_str(self):
        self.assertEqual(str(self.provider), "Test Provider")

    def test_bus_stop_str(self):
        self.assertEqual(str(self.bus_stop), "12345 - Test Bus Stop")

    def test_bus_str(self):
        self.assertEqual(str(self.bus), "TEST001")

    def test_bus_route_str(self):
        expected_str = f"12345 - Test Bus Stop - TEST001 - {self.bus_route.arrival_time}"
        self.assertEqual(str(self.bus_route), expected_str)

    def test_notification_str(self):
        self.assertEqual(str(self.notification), "Test Notification")

    # Add more tests as needed for your models

    def tearDown(self):
        # Clean up the test data
        self.provider.delete()
        self.bus_stop.delete()
        self.bus.delete()
        self.bus_route.delete()
        self.notification.delete()
