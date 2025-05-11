from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .utils import *
import random
from django.contrib import messages
from .filters import *

def landing(request):
    return render(request, 'HireCar/landing.html')

def contact(request):
    return render(request, 'HireCar/contact.html')

def about(request):
    return render(request, 'HireCar/about.html')

def services(request):
    return render(request, 'HireCar/services.html')

def host(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  # 👈 Assign the current user as owner
            car.save()
            return redirect('landing')
    else:
        form = CarForm()
    return render(request, 'HireCar/host.html', {'form': form})



def hire(request):
    search_query = request.GET.get('search', '')
    car_queryset = Car.objects.all()

    # Search filter (make or model)
    if search_query:
        car_queryset = car_queryset.filter(
            models.Q(make__icontains=search_query) |
            models.Q(model__icontains=search_query)
        )

    # Apply additional filters from CarFilter
    car_filter = CarFilter(request.GET, queryset=car_queryset)
    filtered_cars = car_filter.qs

    return render(request, 'HireCar/hire.html', {
        'car': filtered_cars,
        'search_query': search_query,
        'car_filter': car_filter,
    })


def profile(request):
    # Get the user's hosted cars and reservations
    hosted_cars = Car.objects.filter(owner=request.user)
    hired_cars = Reservation.objects.filter(user=request.user)
    try:
        profile = Profile.objects.get(user=request.user) 
    except Profile.DoesNotExist:
        profile = None

    # Pass the actual cars and reservations to the template
    return render(request, 'HireCar/profile.html', {
        'hosted_cars': hosted_cars,
        'hired_cars': hired_cars,
        'profile':profile,
    })

def profile_upload(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # 👈 Assign the current user
            profile.save()
            return redirect('profile')  # Redirect after successful upload
    else:
        form = ProfileUpdateForm()
    return render(request, 'HireCar/update.html', {'form': form})

def details(request, id):
    car = get_object_or_404(Car, pk=id)
    form = ReservationForm()

    # Check if the car is available
    if not car.availability:
        # Pass an error message to the template if the car is not available
        return render(request, 'HireCar/details.html', {'car': car, 'form': form, 'error_message': 'This car is not available for reservation.'})

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.car = car  # Connect the reservation with the car
            reservation.user = request.user  # Assign the current user as renter
            reservation.save()

            # Notify the car owner (host) about the reservation
            host = car.owner
            notification_message = f"Your car {car.make} {car.model} has been reserved by {request.user.full_name}. Please confirm the reservation."
            Notification.objects.create(user=host, message=notification_message, reservation=reservation)

            return redirect('landing')

    return render(request, 'HireCar/details.html', {'car': car, 'form': form})



def update_car(request, id):
    car = get_object_or_404(Car, pk=id)
    form = CarForm(instance=car)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('profile')  # You may want to redirect to profile to see updated details
    return render(request, 'HireCar/update.html', {'form': form})

def delete_car(request, id):
    car = get_object_or_404(Car, pk=id)
    if request.method == 'POST':
        car.delete()
        return redirect('profile')
    
def update_reservation(request, id):
    reservation = get_object_or_404(Reservation, pk=id)
    form = ReservationForm(instance=reservation)
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('profile')  # You may want to redirect to profile to see updated details
    return render(request, 'HireCar/update.html', {'form': form})

def delete_reservation(request, id):
    reservation = get_object_or_404(Reservation, pk=id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('profile')

def login_signup_view(request):
    if request.method == 'POST':
        if 'full_name' in request.POST:
            # Signup form submitted
            signup_form = SignupForm(request.POST)
            login_form = LoginForm()
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = True  # Directly activate user
                user.is_staff = False
                user.is_superuser = False
                user.save()

                auth_login(request, user)  # Log the user in after signup
                messages.success(request, 'Account created and logged in successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Signup failed. Please correct the errors below.')
        else:
            # Login form submitted
            login_form = LoginForm(request, data=request.POST)
            signup_form = SignupForm()
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('landing')
            else:
                messages.error(request, "Invalid login credentials. Please try again.")
    else:
        signup_form = SignupForm()
        login_form = LoginForm()

    return render(request, 'login.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })


def notification_list(request):
    # Fetch all notifications for the logged-in user, ordered by the latest
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'notifications': notifications,
    }
    return render(request, 'HireCar/notification_list.html', context)


def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    # Mark the notification as read
    notification.mark_as_read()

    # If the notification is related to a reservation, notify the renter to make the payment
    if notification.reservation:
        reservation = notification.reservation
        renter = reservation.user
        payment_message = f"Your reservation for {reservation.car.make} {reservation.car.model} has been confirmed by the host. Please proceed with the payment."
        Notification.objects.create(user=renter, message=payment_message, reservation=reservation)

    # Redirect back to the notification list or wherever appropriate
    return redirect('notification_list')


def mark_all_as_read(request):
    # Mark all unread notifications as read
    notifications = Notification.objects.filter(user=request.user, read=False)
    notifications.update(read=True)

    # Redirect back to the notification list or homepage
    return redirect('notification_list')

def payment_page(request):
    return render(request, 'HireCar/payment_page.html')



'''
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

def verify_otp(request):
    email = request.session.get('email')
    if not email:
        return redirect('signup')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            try:
                otp_record = EmailOTP.objects.filter(email=email).latest('created_at')
                if otp_record.is_expired():
                    return render(request, 'HireCar/otp.html', {'form': form, 'error': 'OTP expired'})
                if otp_record.otp == otp_input:
                    user = User.objects.get(email=email)
                    auth_login(request, user)
                    return redirect('landing')
                else:
                    return render(request, 'HireCar/otp.html', {'form': form, 'error': 'Invalid OTP'})
            except EmailOTP.DoesNotExist:
                return redirect('signup')
    else:
        form = OTPForm()
    return render(request, 'HireCar/otp.html', {'form': form})
'''