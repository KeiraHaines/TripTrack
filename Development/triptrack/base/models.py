from django.db import models
from django.contrib.auth.models import User

# Tuple of choices for transport types
tupTran = [
    ('car', 'Car'),
    ('bus', 'Bus'),
    ('bike', 'Bike'),
    ('train','Train'),
    ('plane','Plane'),
    ('other', 'Other'),
]

class Transport(models.Model):
    """
    Represents a mode of transportation for a trip leg.
    """
    strTran = models.CharField(max_length=100, choices=tupTran, null=True, blank=True)

    def __str__(self):
        return self.strTran

class Destination(models.Model):
    """
    Represents a destination or location in a trip.
    """
    strLoc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.strLoc

class Trip(models.Model):
    """
    Represents a complete trip, including name, start and end dates, and associated user.
    """
    strTripName = models.CharField(max_length=50)
    intStartDate = models.DateField()
    intEndDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Event {self.id}"

class TripLeg(models.Model):
    """
    Represents a leg of a trip, including the associated trip, destination, and mode of transport.
    """
    dictTripLst = models.ForeignKey(Trip, on_delete=models.CASCADE)
    strLoc = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, max_length=50)
    strTran = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Leg: {self.id}"

class ChecklistItem(models.Model):
    """
    Represents an item in a trip's checklist, including the associated trip, item title, and completion status.
    """
    dictTripLst = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title  # Changed from self.dictTripLst to self.title for better representation