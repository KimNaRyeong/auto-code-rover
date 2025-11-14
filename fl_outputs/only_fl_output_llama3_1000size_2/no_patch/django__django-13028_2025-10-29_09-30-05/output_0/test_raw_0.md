Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.utils import NotSupportedError

os.environ['DJANGO_SETTINGS_MODULE'] = 'adminpricing.settings'

django.setup()

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
    date_created = models.DateTimeField(null=True, default=django.utils.timezone.now)
    metadata_type = models.ForeignKey(
        ProductMetaDataType, null=False, blank=False, on_delete=models.CASCADE
    )

    class Meta:
        app_label = "adminpricing"
        verbose_name = _("product meta data")
        verbose_name_plural = _("product meta datas")

def main():
    try:
        product_meta_data_type = ProductMetaDataType.objects.create(label='test', filterable=True)
        product_meta_data = ProductMetaData(metadata_type=product_meta_data_type, value="Dark Vador")
        product_meta_data.save()
        ProductMetaData.objects.filter(value="Dark Vador", metadata_type=product_meta_data_type)
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

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
    main()
```

This script sets up the necessary models, creates a `ProductMetaDataType` and a `ProductMetaData`, and then tries to filter `ProductMetaData` objects. If the issue is present (i.e., the query raises a `NotSupportedError`), it prints the stack trace using the provided function and raises an `AssertionError`.