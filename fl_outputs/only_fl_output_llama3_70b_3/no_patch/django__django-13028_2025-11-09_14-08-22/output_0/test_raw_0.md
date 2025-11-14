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

from reproducer.models import ProductMetaDataType, ProductMetaData

try:
    # Try to filter with a metadata_type that has filterable=False
    brand_metadata = ProductMetaDataType.objects.create(label="Brand", filterable=False)
    ProductMetaData.objects.filter(value="Dark Vador", metadata_type=brand_metadata)
except NotSupportedError as e:
    print_stacktrace(e)
    assert False, "Issue is present"
else:
    print("Issue is fixed")
    sys.exit(0)
```
This script defines the two models `ProductMetaDataType` and `ProductMetaData`, creates a database table for them, and then tries to filter `ProductMetaData` with a `metadata_type` that has `filterable=False`. If the issue is present, it will raise a `NotSupportedError` and print the stack trace using the provided function. If the issue is fixed, it will simply print "Issue is fixed" and exit with code 0.

Note that you'll need to create a `reproducer/settings.py` file with the necessary Django settings for this script to work. You can use the following minimal settings:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'reproducer.apps.ReproducerConfig',
]

REPRODUCER_APP_NAME = 'reproducer'
```