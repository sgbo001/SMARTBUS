from django.db import models

class Provider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class BusStop(models.Model):
    stop_point = models.BigIntegerField(unique=True)
    common_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.stop_point} - {self.common_name}"

class Bus(models.Model):
    bus_id = models.CharField(max_length=20, unique=True)
    stop_points = models.ManyToManyField(BusStop)
    bus_providers = models.ManyToManyField(Provider)

    def __str__(self):
        return self.bus_id

class BusRoute(models.Model):
    id = models.AutoField(primary_key=True)
    arrival_time = models.TimeField(verbose_name="Arrival Time")
    bus_id = models.CharField(max_length=20)
    stop_point = models.BigIntegerField(max_length=20)
    common_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.stop_point} - {self.common_name} - {self.bus_id} - {self.arrival_time}"
    
from django.db import models

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
