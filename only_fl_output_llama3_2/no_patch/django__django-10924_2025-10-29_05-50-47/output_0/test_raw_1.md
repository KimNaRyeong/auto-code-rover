Here is the reproducer script:

```python
import os
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured

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
    settings.configure()
except ImproperlyConfigured as e:
    print_stacktrace(e)
    exit(1)
```

This script attempts to configure the Django settings, which should raise an `ImproperlyConfigured` exception if the settings are not properly configured. If this exception is raised, it will be caught and printed along with its stack trace. The script then exits with code 1.

To run this script, save it in a file named `reproducer.py` at the root of your project and execute it using `python3 reproducer.py`.