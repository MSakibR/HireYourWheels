import os
import sys

# প্রজেক্টের রুট ডিরেক্টরিকে Python Path-এ যুক্ত করা
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HireYourWheels_Project.settings')

app = get_wsgi_application()
