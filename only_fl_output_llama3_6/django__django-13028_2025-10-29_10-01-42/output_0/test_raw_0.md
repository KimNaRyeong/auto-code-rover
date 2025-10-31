Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError

# Define the models
class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Produit', null=False, blank=False, on_delete=models.CASCADE)
    value = models.TextField(null=False, blank=False)
    marketplace = models.ForeignKey('Plateforme', null=False, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default=models.timezone.now)
    metadata_type = models.ForeignKey(ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE)

# Create the models
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'  # Replace with your settings file
import django
django.setup()

try:
    # Try to reproduce the issue
    ProductMetaDataType.objects.create(label='test', filterable=True)
    metadata_type = ProductMetaDataType.objects.get(label='test')
    product_metadata = ProductMetaData(metadata_type=metadata_type)
    product_metadata.save()
    ProductMetaData.objects.filter(metadata_type=metadata_type).first()
except NotSupportedError as e:
    # Print the stack trace
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
finally:
    # Exit with code 0 when the issue is fixed
    print("Issue not present, exiting with code 0.")
    exit(0)

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
    python reproducer.py
```

This script creates the models, saves a `ProductMetaDataType` instance and then tries to filter `ProductMetaData` instances by their metadata type. If the issue is present (i.e., a `NotSupportedError` is raised), it prints the stack trace and raises an `AssertionError`.