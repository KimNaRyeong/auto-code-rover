Here is the reproducer script:

```python
import os
from django.db import models
from django.db.utils import NotSupportedError
from django.db.models.query import Q
from django.db.models.manager import Manager
from django.db.models.query_utils import Q as QuerySetQ
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
    settings.configure()
    try:
        ProductMetaDataType.objects.filter(metadata_type__filterable=True)
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script should be run with `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.