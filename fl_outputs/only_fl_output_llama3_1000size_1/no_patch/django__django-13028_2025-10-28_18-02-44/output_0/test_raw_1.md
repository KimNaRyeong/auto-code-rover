Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError
from django.conf import settings

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

# Set the DJANGO_SETTINGS_MODULE environment variable
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

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before importing Django. This should allow the models to be defined and the filter operation to be executed without raising an error.

Please note that you need to have a `settings.py` file in your project's root directory for this script to work.