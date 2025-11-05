Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

from django.db import models
from django.db.utils import NotSupportedError

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

def test_issue():
    ProductMetaDataType.objects.create(label='Test', filterable=False)
    ProductMetaData.objects.create(value='Dark Vador', metadata_type=ProductMetaDataType.objects.get(label='Test'))

    try:
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
This script creates the necessary models, inserts some data, and then tries to filter `ProductMetaData` objects with a `metadata_type` that has `filterable=False`. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.