Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.db import models
from django.db.utils import NotSupportedError

# Define the models
class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

# Configure Django settings
settings.configure(
    INSTALLED_APPS=['reproducer'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

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

try:
    # Create the database tables
    models.Model.__subclasses__()

    # Create a ProductMetaDataType instance
    brand_metadata = ProductMetaDataType.objects.create(label="Brand", filterable=False)

    # Filter ProductMetaData with a metadata_type that has filterable=False
    ProductMetaData.objects.filter(value="Dark Vador", metadata_type=brand_metadata)

    print("Issue is fixed!")
    sys.exit(0)
except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
```
This script defines the two models `ProductMetaDataType` and `ProductMetaData`, configures Django settings, creates a database table for them, and then tries to filter `ProductMetaData` with a `metadata_type` that has `filterable=False`. If the issue is present, it will raise an `AssertionError` with a stack trace of the error. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.

Please save this script as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.