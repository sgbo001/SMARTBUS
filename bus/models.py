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

class PostCode(models.Model):
    post_code = models.CharField(max_length=10, unique=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    stop_point = models.OneToOneField(BusStop, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_code

class Bus(models.Model):
    bus_id = models.CharField(max_length=20, unique=True)
    stop_points = models.ManyToManyField(BusStop)
    bus_providers = models.ManyToManyField(Provider)

    def __str__(self):
        return self.bus_id
