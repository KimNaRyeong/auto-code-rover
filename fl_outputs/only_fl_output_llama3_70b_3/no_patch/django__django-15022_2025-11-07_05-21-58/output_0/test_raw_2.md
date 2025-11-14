Here is a new `reproducer.py` file that should reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import models
from django.contrib import admin

# Define the settings
settings.configure(
    INSTALLED_APPS=['django.contrib.admin', 'django.contrib.contenttypes'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

# Define the models
class Client(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    contact_person = models.CharField(max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

# Define the admin options
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

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

def main():
    # Create the database tables
    setup_test_environment()

    # Create some test data
    for i in range(10907):
        Client.objects.create(name=f"Client {i}")
    for i in range(16952):
        client_office = ClientOffice(client=Client.objects.get(name="Client 0"), name=f"Client Office {i}")
        client_office.save()

    # Create the admin instance
    admin.site.register(Client, ClientAdmin)

    # Perform a search query with multiple words
    try:
        request = {'q': 'word1 word2 word3 word4'}
        cl = ClientAdmin(Client, admin.site)
        qs = cl.get_queryset(request)
        for i in range(10):  # Simulate the issue by adding more joins
            qs = qs.filter(contact_person__contains='word')
        result_count = len(qs)  # This should raise an AssertionError if the issue is present
        assert result_count < 1000, "Issue is present"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```
This script defines the necessary settings, models, and admin options, creates some test data, and then performs a search query with multiple words. It also simulates the issue by adding more joins to the queryset. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.

Please note that this script uses an in-memory SQLite database for testing purposes.