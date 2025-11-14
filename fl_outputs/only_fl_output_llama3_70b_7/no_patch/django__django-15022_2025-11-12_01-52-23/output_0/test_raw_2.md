Here is the revised `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.db import models
from django.contrib import admin

# Configure Django settings
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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

# Define admin options
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name2', 'contact_person', 'clientoffice__name', 'clientoffice__name2')

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

if __name__ == "__main__":
    try:
        # Initialize Django
        setup_test_environment()
        
        # Create test data
        Client.objects.create(name="Client 1", name2="Unofficial 1")
        ClientOffice.objects.create(name="Office 1", client=Client.objects.get(name="Client 1"))
        
        # Register models with admin
        admin.site.register(Client, ClientAdmin)
        
        # Perform search query with multiple words
        qs = Client.objects.all()
        for word in ["word1", "word2", "word3", "word4"]:
            qs = qs.filter(models.Q(name__icontains=word) | 
                             models.Q(name2__icontains=word) | 
                             models.Q(contact_person__icontains=word) | 
                             models.Q(clientoffice__name__icontains=word) | 
                             models.Q(clientoffice__name2__icontains=word))
        
        # Check if the query is too complex
        sql, params = qs.query.sql_with_params()
        if sql.count("JOIN") > 5:
            raise AssertionError("Unnecessary joins in admin changelist query")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script initializes Django, creates test data, registers the models with the admin site, performs a search query with multiple words, and checks if the resulting SQL query has too many joins. If it does, it raises an `AssertionError` with a stack trace of the issue.