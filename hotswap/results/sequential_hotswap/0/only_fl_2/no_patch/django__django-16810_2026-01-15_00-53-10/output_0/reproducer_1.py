import os
import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _
from django.core.wsgi import get_wsgi_application


def home(request):
    """A simple view that returns a HttpResponse."""
    return HttpResponse("Hello, world!")


# Define the Django application settings
settings.configure(
    SECRET_KEY=get_random_secret_key(),
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    LANGUAGES=[
        ('en', _('English')),
        ('fr', _('French')),
    ],
    LANGUAGE_CODE='fr', # Set the default language to French (not English).
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    }],
    PREFIX_DEFAULT_LANGUAGE=False, # This setting is crucial for reproducing the issue.
)

# URL Configuration
urlpatterns = [
    path('', home, name='home'),
]

def print_stacktrace(e: Exception):
    """A function to print the stack trace of the exception."""
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_test():
    """Run the test to either reproduce the issue or confirm it's fixed."""
    os.environ["DJANGO_SETTINGS_MODULE"] = "__main__"
    application = get_wsgi_application()  # Initialize the WSGI application
    from django.test import Client  # Import here due to the need for Django setup
    client = Client()

    try:
        # Request the homepage without language prefix
        response = client.get('/')
        # Expecting HTTP 200 status code, otherwise assuming the issue is present
        assert response.status_code == 200, "Should return 200 OK for the homepage without language prefix."
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code indicating a failure to reproduce or an error was encountered

    print("Test passed: The issue could not be reproduced, indicating it might be fixed.")
    sys.exit(0)

if __name__ == '__main__':
    try:
        run_test()
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)
