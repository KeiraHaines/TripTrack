from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NewTrip(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} on {self.date}"