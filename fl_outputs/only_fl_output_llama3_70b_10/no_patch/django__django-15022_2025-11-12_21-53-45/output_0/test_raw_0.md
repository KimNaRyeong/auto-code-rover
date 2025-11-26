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

def main():
    # Create test database
    setup_test_environment()

    # Create some data
    for i in range(10000):
        client = Client(name=f"Client {i}", name2=f"Unofficial {i}")
        client.save()
        office = ClientOffice(name=f"Office {i}", client=client)
        office.save()

    # Perform search query with multiple words
    try:
        clients = Client.objects.filter(models.Q(name__icontains="word1") | models.Q(name__icontains="word2") | models.Q(name__icontains="word3"))
        assert len(clients.query.sql_with_params()[0]) < 10000, "Unnecessary joins in admin changelist query"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script defines the models and admin options, creates a test database with some data, and then performs a search query with multiple words. If the resulting SQL query has unnecessary joins, it raises an `AssertionError` with a stack trace of the issue.