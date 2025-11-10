Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

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

try:
    from django.test import TestCase
except ImportError as e:
    print_stacktrace(e)
    exit(1)

try:
    admin.site.register(SpecialJournalist, SpecialJournalistAdmin)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will raise an `AssertionError` and print a stack trace.