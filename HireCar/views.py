from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,template_name='HireCar\home.html')
def profile(request):
    return render(request,template_name='HireCar\profile.html')
def history(request):
    return render(request,template_name='HireCar\history.html')