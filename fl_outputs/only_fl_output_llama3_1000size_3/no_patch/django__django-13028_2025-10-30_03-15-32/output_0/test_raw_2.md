Here is the reproducer script:

```python
import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import NotSupportedError
from functools import wraps

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

def check_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotSupportedError as e:
            print_stacktrace(e)
            raise AssertionError("Issue should not be present")
        except ImproperlyConfigured as e:
            print_stacktrace(e)
            raise AssertionError("Issue should not be present")
    return wrapper

@check_issue
def reproduce_issue():
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

    try:
        ProductMetaData.objects.filter(metadata_type__filterable=False)
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be present")
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be present")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates the models, sets up Django by setting the `DJANGO_SETTINGS_MODULE` environment variable and calling `django.setup()`, and then tries to filter `ProductMetaData` objects based on their `metadata_type`. If the issue is present, it will catch the `NotSupportedError` or `ImproperlyConfigured` exceptions, print the stack trace using the provided function, and then raise an `AssertionError`.