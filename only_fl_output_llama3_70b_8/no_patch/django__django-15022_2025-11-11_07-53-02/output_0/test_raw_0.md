Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.db import models
from django.contrib import admin
from django.test.utils import setup_test_environment

# Define models
class Client(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    contact_person = models.CharField(max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

# Define admin options
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

# Register models with admin
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientOffice)

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

def reproduce_issue():
    # Create test data
    for i in range(10000):
        Client.objects.create(name=f"Client {i}")
        ClientOffice.objects.create(name=f"Client Office {i}", client_id=i+1)

    # Perform search query with multiple words
    try:
        admin.site._registry[Client].get_queryset(admin.site._registry[Client]).filter(
            models.Q(name__icontains='word1') |
            models.Q(name2__icontains='word2') |
            models.Q(contact_person__icontains='word3') |
            models.Q(clientoffice__name__icontains='word4')
        )
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    setup_test_environment()
    reproduce_issue()
    sys.exit(0)
```
This script defines the models and admin options, creates test data, and performs a search query with multiple words. If the issue is present, it raises an `AssertionError` with a stack trace of the error. If the issue is fixed, the script exits with code 0.

Note that you'll need to create a `reproducer/settings.py` file with the necessary Django settings for this script to work. You can use the following minimal settings:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'reproducer'
]

SECRET_KEY = 'secret_key_here'
```