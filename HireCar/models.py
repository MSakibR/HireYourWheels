from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class CarType(models.Model):
    name = models.CharField(max_length=100) #(SUV, Sedan)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    c_id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
        editable=False,
    )
    image = models.ImageField(upload_to='car_images/img',blank=True, null=True)
    name = models.CharField(max_length=100)  #(Toyota,BMW)
    model_year = models.IntegerField()
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    status_choices = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved')
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')

    def __str__(self):
        return f"{self.name} ({self.model_year})"


class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
