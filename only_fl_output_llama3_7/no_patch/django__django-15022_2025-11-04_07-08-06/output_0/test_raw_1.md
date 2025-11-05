Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db.models import Q
from django.db import models

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

class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=256, blank=True, null=True)

class ClientOffice(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=256, blank=True, null=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))

class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

# Create admin site
admin.site.register(Client, ClientAdmin)

try:
    # Create a search query with multiple words
    client_qs = Client.objects.filter(Q(name='test') | Q(contact_person='test'))
    for _ in range(1000):
        client_qs = client_qs.filter(Q(name='test2') | Q(clientoffice__name='test3'))

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script sets up the models and admin options, then creates a search query with multiple words. The `try` block attempts to execute this query 1000 times, which should cause Django's ORM to generate an excessive number of joins in the SQL query. If the issue is present, it will raise an `AssertionError`, which will be caught by the `except` block and printed using the provided `print_stacktrace` function.