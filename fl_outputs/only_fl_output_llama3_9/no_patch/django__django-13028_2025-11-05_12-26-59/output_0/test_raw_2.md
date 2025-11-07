Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError
from django.conf import settings

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

def main():
    class ProductMetaDataType(models.Model):
        label = models.CharField(max_length=255, unique=True, blank=False, null=False)
        filterable = models.BooleanField(default=False, verbose_name=_("filterable"))

    class ProductMetaData(models.Model):
        id = models.BigAutoField(primary_key=True)
        product = models.ForeignKey(
            'Produit', null=False, blank=False, on_delete=models.CASCADE
        )
        value = models.TextField(null=False, blank=False)
        marketplace = models.ForeignKey(
            'Plateforme', null=False, blank=False, on_delete=models.CASCADE
        )
        date_created = models.DateTimeField(null=True, default=settings.timezone.now)
        metadata_type = models.ForeignKey(
            ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE
        )

    try:
        ProductMetaData.objects.filter(metadata_type__filterable=True)
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script should be run with `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.