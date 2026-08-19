import os
import sys

# Current directory & parent directory path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HireYourWheels_Project.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
