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

# Create test data
def create_test_data():
    for i in range(10907):
        Client.objects.create(name=f"Client {i}", name2=f"Client 2 {i}")
    for i in range(16952):
        client = Client.objects.order_by('?')[0]
        ClientOffice.objects.create(name=f"Client Office {i}", client=client)

# Reproduce the issue
def reproduce_issue():
    try:
        # Create test data
        create_test_data()

        # Register models with admin
        admin.site.register(Client, ClientAdmin)

        # Setup test environment
        setup_test_environment()

        # Perform search query
        from django.contrib.admin.views.main import ChangeList
        cl = ChangeList(request={}, model=Client, list_display=['name'])
        qs = cl.get_query_set()
        for word in ["word1", "word2", "word3", "word4"]:
            qs = qs.filter(models.Q(name__icontains=word) | models.Q(name2__icontains=word) | models.Q(contact_person__icontains=word) | models.Q(clientoffice__name__icontains=word) | models.Q(clientoffice__name2__icontains=word))

        # Check if the query is too complex
        sql = str(qs.query)
        if sql.count("JOIN") > 5:
            raise AssertionError("Unnecessary joins in admin changelist query")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```
This script defines the models, creates test data, registers the models with the admin interface, and performs a search query with multiple words. It then checks if the resulting SQL query has too many joins (more than 5). If it does, it raises an `AssertionError` with a stack trace of the issue.