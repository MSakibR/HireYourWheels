from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import EmailOTP
from .forms import EmailForm, OTPForm
import random
from .utils import generate_and_send_otp

# Create your views here.

def home(request):
    car = Car.objects.all()
    context={
        'car': car
    }
    return render(request, template_name ='HireCar\home.html',context=context) 

def profile(request):
    cartype = CarType.objects.all()
    context = {
        'type': cartype
    }
    return render(request, template_name ='HireCar\profile.html',context=context) 

def details(request,id):
    car = Car.objects.get(pk = id)
    context = {
        'car':car,
    }
    return render(request, template_name ='HireCar\details.html',context=context) 


def upload_car(request):
   form = CarForm()
   if request.method == 'POST':
       form = CarForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('home')  # Redirect after saving the car
   context = {'form': form}
   return render(request, template_name='HireCar/car_form.html', context=context)

def update_car(request, id):
   car = Car.objects.get(pk=id)
   form = CarForm(instance=car)
   if request.method == 'POST':
       form = CarForm(request.POST, request.FILES, instance=car)
       if form.is_valid():
           form.save()
           return redirect('home')  # Redirect after updating the car
   context = {'form': form}
   return render(request, template_name='HireCar/car_form.html', context=context)

def delete_car(request, id):
    car = get_object_or_404(Car, pk=id)  # Use get_object_or_404 to handle invalid IDs gracefully
    if request.method == 'POST':
        car.delete()
        return redirect('home')  # Redirect to home after deletion


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            email = user.email
            otp = generate_and_send_otp(email)  # Generate & send OTP
            EmailOTP.objects.create(email=email, otp=otp)  # Save OTP in DB
            request.session['email'] = email  # Store email in session
            return redirect('verify_otp')  # Redirect to OTP verification
    else:
        form = SignupForm()
    return render(request, 'HireCar/signup.html', {'form': form, 'hide_nav_footer': True})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'HireCar/login.html', {'form': form, 'hide_nav_footer': True})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def generate_otp():
    return str(random.randint(100000, 999999))

def verify_otp(request):
    email = request.session.get('email')  # Retrieve the email from the session
    if not email:
        return redirect('signup')  # If no email, redirect to signup

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            try:
                otp_record = EmailOTP.objects.filter(email=email).latest('created_at')
                if otp_record.is_expired():
                    return render(request, 'HireCar/verify_otp.html', {'form': form, 'error': 'OTP expired'})
                if otp_record.otp == otp_input:
                    # OTP is valid, log the user in
                    user = authenticate(email=email)  # Authenticate the user by email
                    if user:
                        login(request, user)  # Log the user in
                        return redirect('home')  # Redirect to home page after login
                    else:
                        return render(request, 'HireCar/verify_otp.html', {'form': form, 'error': 'User not found'})
                else:
                    return render(request, 'HireCar/verify_otp.html', {'form': form, 'error': 'Invalid OTP'})
            except EmailOTP.DoesNotExist:
                return redirect('signup')  # If OTP record doesn't exist, redirect to signup
    else:
        form = OTPForm()
    return render(request, 'HireCar/verify_otp.html', {'form': form})