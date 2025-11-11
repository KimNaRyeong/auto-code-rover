Here is the reproducer script:

```python
import os
from django.db import models
from django.utils import timezone
from django.db.utils import NotSupportedError

os.environ['DJANGO_SETTINGS_MODULE'] = 'adminpricing.settings'

def main():
    try:
        from adminpricing.models import ProductMetaDataType, ProductMetaData

        product_meta_data_type = ProductMetaDataType.objects.create(label='test', filterable=False)
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