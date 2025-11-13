Here is the revised `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import models
from django.contrib import admin

# Configure Django settings
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['reproducer'],
)

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
    # Create test database
    setup_test_environment()

    # Import models to register with admin
    from reproducer import Client, ClientOffice

    # Register models with admin
    admin.site.register(Client, ClientAdmin)
    admin.site.register(ClientOffice)

    # Create some data
    for i in range(10000):
        client = Client(name=f"Client {i}", name2=f"Unofficial {i}")
        client.save()
        office = ClientOffice(name=f"Office {i}", client=client)
        office.save()

    # Perform search query with multiple words
    try:
        from django.contrib.admin.views.main import ChangeList
        cl = ChangeList(request={}, model=Client, list_display=('name',))
        qs = cl.get_query_set()
        for word in ["word1", "word2", "word3"]:
            qs = qs.filter(models.Q(name__icontains=word) | models.Q(name2__icontains=word) | models.Q(contact_person__icontains=word) | models.Q(clientoffice__name__icontains=word) | models.Q(clientoffice__name2__icontains=word))
        sql_query = str(qs.query)
        if "JOIN" in sql_query:
            raise AssertionError("Unnecessary joins in admin changelist query")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script configures Django settings, defines the models and admin options, creates a test database with some data, and then performs a search query with multiple words using the `ChangeList` class from Django's admin views. If the resulting SQL query has unnecessary joins, it raises an `AssertionError` with a stack trace of the issue.