from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from HireCar import views as Hire_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Hire_views.landing, name='landing'),
    path('contact', Hire_views.contact, name='contact'),
    path('about', Hire_views.about, name='about'),
    path('services', Hire_views.services, name='services'),

    path('login/', Hire_views.login_signup_view, name='login'),  
   path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),

    path('host/', Hire_views.host, name='host'),
    path('hire/', Hire_views.hire, name='hire'),
    path('profile/', Hire_views.profile, name='profile'),
    path('profile/upload', Hire_views.profile_upload, name='profile_upload'),
    path('details/<uuid:id>/', Hire_views.details, name='details'),

    #path('upload/', Hire_views.upload_car, name='upload_car'),
    path('update/<uuid:id>/', Hire_views.update_car, name='update_car'),
    path('delete/<uuid:id>/', Hire_views.delete_car, name='delete_car'),
    path('update_reservation/<uuid:id>/', Hire_views.update_reservation, name='update_reservation'),
    path('delete_reservation/<uuid:id>/', Hire_views.delete_reservation, name='delete_reservation'),
    #path('profile/update/', Hire_views.update_profile, name='update_profile'),

    #path('verify/', Hire_views.verify_otp, name='verify_otp'),
    path('notifications/', Hire_views.notification_list, name='notification_list'),
    path('notifications/mark_as_read/<uuid:notification_id>/', Hire_views.mark_as_read, name='mark_as_read'),
    path('notifications/mark_all_as_read/', Hire_views.mark_all_as_read, name='mark_all_as_read'),
    path('payment/', Hire_views.payment_page, name='payment_page'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
