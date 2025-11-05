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
    client = models.ForeignKey(Client, verbose_name='client')

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
    # Set up Django test environment
    setup_test_environment()

    # Create admin site
    admin.site.register(Client, ClientAdmin)

    # Create some sample data
    for i in range(10000):
        client = Client(name=f"Client {i}", name2=f"Client 2 {i}")
        client.save()
        client_office = ClientOffice(name=f"Client Office {i}", client=client)
        client_office.save()

    # Perform search query with multiple words
    try:
        admin.site._registry[Client].get_queryset(admin.site._registry[Client]).filter(models.Q(name__icontains='word1') | models.Q(name__icontains='word2') | models.Q(name__icontains='word3'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    main()
```
This script defines the `Client` and `ClientOffice` models, sets up a Django test environment, creates some sample data, and then performs a search query with multiple words using the `filter()` method. If an exception occurs during the search query, it prints the stack trace using the provided `print_stacktrace()` function and raises an `AssertionError`.