Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.db.utils import NotSupportedError

# Create a new Django project and app
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
import django
django.setup()

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField(null=False, blank=False)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

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
    # Create a instance of ProductMetaDataType
    brand_metadata = ProductMetaDataType.objects.create(label="Brand")

    # Filter ProductMetaData with a metadata_type that has filterable=False attribute
    ProductMetaData.objects.filter(value="Dark Vador", metadata_type=brand_metadata)

except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    sys.exit(0)
```
This script creates two Django models, `ProductMetaDataType` and `ProductMetaData`, with a foreign key relationship between them. It then creates an instance of `ProductMetaDataType` and tries to filter `ProductMetaData` using that instance as the RHS of the filter clause.

If the issue is present, the script will raise a `NotSupportedError` exception, which will be caught and printed along with its stack trace using the `print_stacktrace` function. The script will then raise an `AssertionError` to indicate that the issue is present.

If the issue is fixed, the script will exit with code 0.