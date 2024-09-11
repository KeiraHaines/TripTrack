from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
# Create your models here.

TRANSPORT_CHOICES = [
        ('car', 'Car'),
        ('bus', 'Bus'),
        ('bike', 'Bike'),
        ('train','Train'),
        ('plane','Plane'),
        ('other', 'Other'),
    ]

class Transport(models.Model):
    
    name = models.CharField(max_length=100, choices=TRANSPORT_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class newTrip (models.Model):

    strTripName = models.CharField(max_length=50)
    intStartDate = models.DateField()
    intEndDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Event {self.id}"
    
class Leg (models.Model):

    trip = models.ForeignKey(newTrip, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, max_length=50)
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Leg: {self.id}"
    
class ChecklistItem(models.Model):
    trip = models.ForeignKey(newTrip, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title