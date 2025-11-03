Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError
from django.db.models.query import Q
from django.db.models.manager import Manager
from django.db.models.query_utils import Q as DjangoQ

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True, blank=False, null=False)
    filterable = models.BooleanField(default=False, verbose_name=_("filterable"))

    class Meta:
        app_label = "adminpricing"
        verbose_name = _("product meta data type")
        verbose_name_plural = _("product meta data types")

class ProductMetaData(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        'Produit', null=False, blank=False, on_delete=models.CASCADE
    )
    value = models.TextField(null=False, blank=False)
    marketplace = models.ForeignKey(
        'Plateforme', null=False, blank=False, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(null=True, default=models.timezone.now)
    metadata_type = models.ForeignKey(
        ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE
    )

    class Meta:
        app_label = "adminpricing"
        verbose_name = _("product meta data")
        verbose_name_plural = _("product meta datas")

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

def reproduce_issue():
    try:
        metadata_type = ProductMetaDataType.objects.create(label="test", filterable=False)
        product_metadata = ProductMetaData(metadata_type=metadata_type)
        product_metadata.save()
        ProductMetaData.objects.filter(metadata_type=metadata_type).first()
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a `ProductMetaDataType` instance with `filterable=False`, then tries to filter `ProductMetaData` instances by this metadata type. If the issue is present, it prints the stack trace and raises an `AssertionError`.