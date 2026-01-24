import os
from django.core.asgi import get_asgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapp.settings')

# Create the ASGI application
application = get_asgi_application()
