import random
from django.core.mail import EmailMessage
from django.conf import settings

def generate_and_send_otp(user_email):
    otp = str(random.randint(100000, 999999))
    subject = 'Your OTP Code'
    body = f'Hello,\n\nYour OTP is: {otp}. Please use it within 5 minutes.'

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
        headers={'Reply-To': 'noreply@hireyourwheels.com'}
    )
    email.send()
    return otp
