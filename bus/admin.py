from django.contrib import admin
from .models import Provider, BusStop, Bus, BusRoute, Notification
# Register your models here.
admin.site.register(Provider)
admin.site.register(BusStop)
admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(Notification)
