Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import django
from django.db import models
from django.db.utils import NotSupportedError

# Create a new Django project and app for testing
os.system("django-admin startproject reproducer_project")
os.chdir("reproducer_project")
os.system("python manage.py startapp reproducer_app")

# Define the models
class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

# Create the database tables
os.system("python manage.py makemigrations reproducer_app")
os.system("python manage.py migrate")

def test_issue():
    from reproducer_app.models import ProductMetaDataType, ProductMetaData

    # Create some data
    ProductMetaDataType.objects.create(label='Test', filterable=False)
    ProductMetaData.objects.create(value='Dark Vador', metadata_type=ProductMetaDataType.objects.get(label='Test'))

    try:
        # Try to filter with a metadata_type that has filterable=False
        ProductMetaData.objects.filter(value="Dark Vador", metadata_type=ProductMetaDataType.objects.get(label='Test'))
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

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

if __name__ == '__main__':
    test_issue()
```
This script creates a new Django project and app, defines the models, creates the database tables, inserts some data, and then tries to filter `ProductMetaData` objects with a `metadata_type` that has `filterable=False`. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.