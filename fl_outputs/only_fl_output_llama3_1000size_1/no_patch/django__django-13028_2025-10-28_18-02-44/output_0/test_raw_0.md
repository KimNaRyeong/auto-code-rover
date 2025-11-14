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
    date_created = models.DateTimeField(null=True, default=models.DateTimeField.now)
    metadata_type = models.ForeignKey(ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE)

# Create the models
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

try:
    # Try to filter ProductMetaData with a metadata_type
    ProductMetaData.objects.filter(metadata_type__filterable=True)
except NotSupportedError as e:
    print_stacktrace(e)
    assert False, "Expected NotSupportedError"

print("Issue not present")
```

This script creates the models and then tries to filter `ProductMetaData` objects based on their `metadata_type`. If the issue is present, it should raise a `NotSupportedError`, which will be caught and an assertion error will be raised.