from django.db import models
from django.contrib.auth.models import *
import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)     # User inactive until OTP verification
        extra_fields.setdefault('is_staff', False)      # Not staff
        extra_fields.setdefault('is_superuser', False)  # Not superuser

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Host', 'Host'),
        ('Hire', 'Hire'),
    )

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Host')

    is_active = models.BooleanField(default=False)  # <- very important: default=False
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username


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
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cars')
    image = models.ImageField(upload_to='car_images/img',blank=True, null=True)
    make = models.CharField(max_length=100)  # Make of the car, e.g., Toyota
    model = models.CharField(max_length=100)  # Model name, e.g., Camry
    year = models.PositiveIntegerField()  # Year of the car
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()  # Number of seats
    transmission = models.CharField(max_length=50)  
    mileage = models.FloatField()  
    fuel_type = models.CharField(max_length=50)  
    features = models.TextField() 
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)  
    availability = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Reservation(models.Model):
    r_id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    dropoff_date = models.DateField()

    def __str__(self):
        return f"Reservation for {self.car} from {self.pickup_date} to {self.dropoff_date}"


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.CASCADE)  # Related reservation (if applicable)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_unread(self):
        self.read = False
        self.save()

    class Meta:
        ordering = ['-timestamp']  # To show the latest notifications first


'''    
class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
'''

