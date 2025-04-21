"""
URL configuration for HireYourWheels_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from HireCar import views as Hire_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', Hire_views.home, name='home'),
    path('profile', Hire_views.profile, name='profile'),
    path('details/<uuid:id>/', Hire_views.details, name='details'),
    path('upload/', Hire_views.upload_car, name='upload_car'),  # URL for uploading a car
    path('Update/<uuid:id>/', Hire_views.update_car, name='update_car'),
    path('delete/<uuid:id>/', Hire_views.delete_car, name='delete_car'),
    path('signup/', Hire_views.signup_view, name='signup'),
    path('', Hire_views.login_view, name='login'),
    path('logout/', Hire_views.logout_view, name='logout'),
    path('verify/', Hire_views.verify_otp, name='verify_otp'),
    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
