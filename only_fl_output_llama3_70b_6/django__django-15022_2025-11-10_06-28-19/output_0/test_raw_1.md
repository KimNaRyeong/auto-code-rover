Here is the revised `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import models
from django.contrib import admin

# Define settings
settings.configure(INSTALLED_APPS=['django.contrib.admin', 'django.contrib.contenttypes'],
                     DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}})

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
    # Setup test environment
    setup_test_environment()

    # Create admin site
    from django.contrib.admin import site
    my_admin_site = site.AdminSite(name='my_admin')

    # Register models with admin site
    my_admin_site.register(Client, ClientAdmin)
    my_admin_site.register(ClientOffice)

    # Create some test data
    for i in range(10000):
        client = Client(name=f"Client {i}", name2=f"Unofficial {i}")
        client.save()
        office = ClientOffice(name=f"Office {i}", client=client)
        office.save()

    # Perform search query with multiple words (>3)
    request = {'q': 'word1 word2 word3 word4'}
    cl = my_admin_site._registry[Client].get_changelist_instance(request)

    try:
        qs = cl.get_query_set()
        if qs.query.sql_with_params()[0].count('JOIN') > 3:
            raise AssertionError("Issue is present")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```
This script defines the settings, models, and admin options, sets up a test environment, creates some test data, and performs a search query with multiple words. If the issue is present (i.e., more than 3 JOINs in the SQL query), it will raise an `AssertionError` and print a stack trace of the issue.