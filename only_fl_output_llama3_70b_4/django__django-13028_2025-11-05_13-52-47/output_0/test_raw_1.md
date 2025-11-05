Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.test import TestCase
from django.db import models

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['__main__'],
)

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

try:
    ProductMetaDataType.objects.create(label='test', filterable=False)
    metadata_type = ProductMetaDataType.objects.get(label='test')
    ProductMetaData.objects.create(value="Dark Vador", metadata_type=metadata_type)
    ProductMetaData.objects.filter(value="Dark Vador", metadata_type=metadata_type)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
```
This script creates the necessary models, inserts some data, and then tries to filter `ProductMetaData` objects with a `metadata_type` that has a `filterable` attribute set to `False`. If the issue is present, it will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, it will print "Issue is fixed" and exit with code 0.