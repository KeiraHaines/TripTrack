from django.contrib import admin
from .models import newTrip, Transport, Leg

# Register your models here.
admin.site.register(newTrip)
admin.site.register(Transport)
admin.site.register(Leg)
