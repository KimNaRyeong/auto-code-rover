Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.db import models
from django.contrib import admin
from django.test.utils import setup_test_environment

# Define the models
class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))

# Define the admin options
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

# Create the admin site and register the models
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientOffice)

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

def reproduce_issue():
    # Create some test data
    for i in range(10000):
        Client.objects.create(name=f'Client {i}', name2=f'Client {i} unofficial')
        ClientOffice.objects.create(name=f'Client Office {i}', client=Client.objects.get(name=f'Client {i}'))

    # Try to search for clients with a query containing several words
    try:
        request = {'q': 'client office unofficial'}
        admin.site.each_context(request)
        changelist = ClientAdmin(Client, admin.site).get_changelist_instance(request)
        changelist.get_query_set()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    setup_test_environment()
    reproduce_issue()
```
This script defines the models and admin options, creates some test data, and then tries to search for clients with a query containing several words. If the issue is present, it will raise an `AssertionError` with a stack trace of the issue.