Here is a revised `reproducer.py` file that should reproduce the issue:
```
import os
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.test import TestCase, RequestFactory

class OrderSearch(ListView):
    """ :view:orders.views.Orders """
    pass

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    import django
    django.setup()

    from django.test.utils import setup_test_environment
    setup_test_environment()

    request_factory = RequestFactory()
    request = request_factory.get('/admin/doc/views/orders.views.Orders/')

    try:
        from django.contrib.admindocs.views import ViewDetailView
        response = ViewDetailView.as_view()(request, 'orders.views.Orders')
        if response.status_code == 404:
            raise AssertionError("Mixed-case views/templates names causes 404 on :view:/:template: directive.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
This script sets the `DJANGO_SETTINGS_MODULE` environment variable to `reproducer.settings`, which should allow Django to find the settings module.

Please create a new file `reproducer/settings.py` with the following contents:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'reproducer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
```
This settings file enables the `admin` and `admindocs` apps, which are required for the issue to occur.

Create a new file `reproducer/urls.py` with the following contents:
```
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]
```
This URL configuration enables the Django admin interface.

Run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace of the issue.