from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
            form.save()
            return redirect('login')
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