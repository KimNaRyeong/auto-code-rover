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
    product = models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE)
    value = models.TextField(null=False, blank=False)
    marketplace = models.ForeignKey('Marketplace', null=False, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default='now')
    metadata_type = models.ForeignKey(ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE)

# Create the models
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
import django
django.setup()

try:
    # Try to filter ProductMetaData with a metadata_type
    product_meta_data_type = ProductMetaDataType.objects.create(label='Test', filterable=True)
    ProductMetaData.objects.filter(metadata_type=product_meta_data_type).first()
except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")
else:
    print("Issue fixed")
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