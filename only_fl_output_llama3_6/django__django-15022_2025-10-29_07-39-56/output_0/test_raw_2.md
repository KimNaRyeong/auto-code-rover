Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db.models import Q
from django.db.models.query import QuerySet

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

# Set up Django environment
django.setup()

admin.autodiscover()

class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))

# Create admin interface
admin.site.register(Client)

def search_client(query):
    qs = Client.objects.all()
    for word in query.split():
        qs = qs.filter(Q(name__icontains=word) | Q(name2__icontains=word) | Q(contact_person__icontains=word) | Q(clientoffice__name__icontains=word) | Q(clientoffice__name2__icontains=word))
    return qs

# Reproduce the issue
query = "test test"
try:
    search_client(query)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
else:
    print("Issue fixed, exiting with code 0")
    exit(0)

```

This script sets up a Django environment, defines the `Client` and `ClientOffice` models, creates an admin interface for the `Client` model, and then attempts to reproduce the issue by searching for clients with a query containing multiple words. If the issue is present, it will print the stack trace and raise an `AssertionError`.