from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .utils import *
import random
from django.contrib import messages

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
    car = Car.objects.all()
    return render(request, 'HireCar/hire.html', {'car': car})

def profile(request):
    # Get the user's hosted cars and reservations
    hosted_cars = Car.objects.filter(owner=request.user)
    hired_cars = Reservation.objects.filter(user=request.user)

    # Pass the actual cars and reservations to the template
    return render(request, 'HireCar/profile.html', {
        'hosted_cars': hosted_cars,
        'hired_cars': hired_cars,
    })


def details(request, id):
    car = get_object_or_404(Car, pk=id)
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.car = car  # Connect the reservation with the car
            reservation.user = request.user  # 👈 Assign the current user as owner
            reservation.save()
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