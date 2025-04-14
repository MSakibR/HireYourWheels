from django.shortcuts import render
from .models import *

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
