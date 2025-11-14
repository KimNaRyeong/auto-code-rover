Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.db.utils import NotSupportedError

# Define the models
class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE)

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

# Create the database tables
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
import django
django.setup()

from reproducer import settings

try:
    # Try to reproduce the issue
    ProductMetaDataType.objects.create(label='Test', filterable=False)
    brand_metadata = ProductMetaDataType.objects.get(label='Test')
    ProductMetaData.objects.filter(value="Dark Vador", metadata_type=brand_metadata)
except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
    sys.exit(0)
```
This script defines the two models `ProductMetaDataType` and `ProductMetaData`, creates a database table for them, and then tries to reproduce the issue by filtering `ProductMetaData` with a `metadata_type` that has a `filterable=False` attribute. If the issue is present, it raises an `AssertionError` with a stack trace of the error. If the issue is fixed, it prints "Issue is fixed" and exits with code 0.

Note that you need to create a `settings.py` file in the same directory as this script, with the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = ['reproducer']
```
This sets up a SQLite database in memory for the test.