Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
    # Try to reproduce the issue
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
    settings.configure()

    ProductMetaDataType.objects.create(label='test', filterable=True)
    metadata_type = ProductMetaDataType.objects.get(label='test')
    product_metadata = ProductMetaData(metadata_type=metadata_type)
    product_metadata.save()
    ProductMetaData.objects.filter(metadata_type=metadata_type).first()

except NotSupportedError as e:
    # Print the stack trace
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")

except ImproperlyConfigured as e:
    # Print the stack trace
    print_stacktrace(e)
    raise AssertionError("Issue not present, exiting with code 0.")
    exit(0)

finally:
    # Exit with code 0 when the issue is fixed
    print("Issue not present, exiting with code 0.")
    exit(0)

if __name__ == "__main__":
    try:
        ProductMetaData.objects.filter(metadata_type=ProductMetaDataType(filterable=False)).first()
    except NotSupportedError as e:
        # Print the stack trace
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")
    else:
        print("Issue not present, exiting with code 0.")
        exit(0)

```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable and then tries to create a model instance. If the issue is present (i.e., a `NotSupportedError` or an `ImproperlyConfigured` exception is raised), it prints the stack trace and raises an `AssertionError`.