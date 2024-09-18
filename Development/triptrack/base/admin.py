# Import necessary Django modules and custom components
from django.contrib import admin
from .models import Trip, Transport, TripLeg, ChecklistItem

# Registers my models to the admin panel.
admin.site.register(Trip)
admin.site.register(Transport)
admin.site.register(TripLeg)
admin.site.register(ChecklistItem)
