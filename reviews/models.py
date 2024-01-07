from django.db import models
from django.contrib.auth.models import User
from bus.models import BusRoute

class Review(models.Model):
    full_name = models.CharField(max_length=255, blank=False)
    stop_point = models.CharField(max_length=255, blank=False)
    common_name = models.CharField(max_length=255, blank=True)
    bus_id = models.CharField(max_length=10, blank=False)
    arrival_time = models.TimeField(verbose_name="Arrival Time", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    RATING_CHOICES = (
        (1, 'Late'),
        (2, 'Somewhat Late'),
        (3, 'On Time'),
        (4, 'Somewhat Early'),
        (5, 'Very Early'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Review by {self.full_name} for {self.bus_id} at {self.arrival_time}"
