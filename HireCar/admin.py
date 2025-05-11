from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([
    CarType, Car, CustomUser,Reservation,Profile,Notification
    ])