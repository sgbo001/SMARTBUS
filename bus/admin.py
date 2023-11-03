from django.contrib import admin
from .models import Provider, BusStop, Bus
# Register your models here.
admin.site.register(Provider)
admin.site.register(BusStop)
admin.site.register(Bus)
