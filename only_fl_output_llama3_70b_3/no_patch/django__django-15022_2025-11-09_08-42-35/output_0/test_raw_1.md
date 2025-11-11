Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import models
from django.contrib import admin

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

# Set up Django settings
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    INSTALLED_APPS=['reproducer'],
    ROOT_URLCONF='reproducer.urls',
)

# Create models
class Client(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    contact_person = models.CharField(max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(max_length=256)
    name2 = models.CharField(max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

# Create admin options
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

try:
    # Set up Django test environment
    setup_test_environment()

    # Create the database tables
    from django.core.management import call_command
    call_command('migrate', verbosity=0)

    # Populate the database with some data
    for i in range(10907):
        Client.objects.create(name=f'Client {i}')
    for i in range(16952):
        client_office = ClientOffice(client=Client.objects.get(pk=i % 10907 + 1), name=f'Client Office {i}')
        client_office.save()

    # Perform the search query
    admin.site.register(Client, ClientAdmin)
    from django.contrib.admin.views.main import Changelist
    cl = Changelist(request={}, model=Client, list_display=['name'])
    qs = cl.get_queryset()
    for word in ['word1', 'word2', 'word3', 'word4']:
        qs = qs.filter(models.Q(name__icontains=word) | models.Q(name2__icontains=word) | models.Q(contact_person__icontains=word) | models.Q(clientoffice__name__icontains=word) | models.Q(clientoffice__name2__icontains=word))

    # Check if the query is too complex
    if qs.query.sql_with_params()[0].count('JOIN') > 5:
        raise AssertionError("Unnecessary joins in admin changelist query")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up Django settings, creates the models, populates the database with some data, and performs a search query with multiple words. It then checks if the resulting SQL query has too many joins (more than 5 in this case). If it does, it raises an `AssertionError` with a stack trace of the issue.