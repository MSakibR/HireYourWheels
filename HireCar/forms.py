from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.forms import *

class CarForm(ModelForm):
   class Meta:
        model = Car
        fields = [
            'image', 'make', 'model', 'year', 'car_type', 'seats',
            'transmission', 'mileage', 'fuel_type', 'features',
            'daily_rate', 'availability'
        ]
        widgets = {
            'features': forms.Textarea(attrs={'rows': 3}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['pickup_date', 'dropoff_date']
        widgets = {
            'pickup_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'pickup-date form-control',
                'required': True,
            }),
            'dropoff_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'dropoff-date form-control',
                'required': True,
            }),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'phone', 'email', 'address', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#e-mail
class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)