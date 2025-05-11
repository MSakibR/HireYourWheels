from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save


@receiver(post_save, sender=Reservation)
def update_car_availability_on_save(sender, instance, **kwargs):
    car = instance.car
    today = date.today()

    # Check if any future or active reservations exist
    has_active_reservations = Reservation.objects.filter(
        car=car,
        dropoff_date__gte=today
    ).exists()

    car.availability = not has_active_reservations
    car.save(update_fields=['availability'])

@receiver(post_delete, sender=Reservation)
def update_car_availability_on_delete(sender, instance, **kwargs):
    car = instance.car
    today = date.today()

    # Check if any other reservations still exist for this car
    has_active_reservations = Reservation.objects.filter(
        car=car,
        dropoff_date__gte=today
    ).exists()

    car.availability = not has_active_reservations
    car.save(update_fields=['availability'])


@receiver(pre_save, sender=Reservation)
def validate_car_availability(sender, instance, **kwargs):
    # Ensure car exists for the reservation
    if not instance.car:
        raise ValidationError(_('This reservation must have a car assigned.'))
    
    # Ensure the car is available for the reservation
    if not instance.car.availability:
        raise ValidationError(_('This car is not available for reservation.'))

    # Ensure pickup date is before dropoff date
    if instance.pickup_date and instance.dropoff_date:
        if instance.pickup_date > instance.dropoff_date:
            raise ValidationError(_('Pickup date must be before dropoff date.'))