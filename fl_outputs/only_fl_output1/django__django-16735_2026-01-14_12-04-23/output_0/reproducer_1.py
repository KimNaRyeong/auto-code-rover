# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import include, path

# Function to print stack trace
def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Minimal Django setup
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='this-is-just-a-dummy-key',
    ALLOWED_HOSTS=['*'],
    USE_I18N=True,
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', 'English'),
        ('de', 'German'),
    ),
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
)
django.setup()

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

def test_view(request):
    return HttpResponse("This is a test view")

urlpatterns = [
    # Non-i18n patterns here if needed
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("test/", test_view),
    prefix_default_language=False,  # This is the focus of the test
)

if __name__ == "__main__":
    try:
        # Ensure Django apps are ready and the setup is complete
        from django.test import Client
        c = Client()
        
        # Request the "/admin/" to see if it redirects or not
        response = c.get('/admin/')
        
        # Asserting directly on status_code 200 to check if it's accessible without redirect
        assert response.status_code == 200, "/admin/ should be directly accessible without redirect"
        print("The issue is not present.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error if the assertion failed, indicating the issue exists
    
    # If everything is okay, exit with 0
    sys.exit(0)
