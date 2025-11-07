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
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    value = models.TextField(null=False, blank=False)
    marketplace = models.ForeignKey('Marketplace', on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, default='now')
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

# Create the models
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

try:
    # Try to filter ProductMetaData with a metadata_type
    ProductMetaData.objects.filter(metadata_type__filterable=False)
except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue should not be present")
```

This script creates the models, sets up Django, and then tries to filter `ProductMetaData` objects based on their `metadata_type`. If the issue is present, it will catch the `NotSupportedError`, print the stack trace using the provided function, and then raise an `AssertionError`.