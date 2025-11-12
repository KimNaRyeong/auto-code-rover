Here is the reproducer script:

```python
import os
import django
from django.db import models

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

django.setup()

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

class Document(models.Model):
    pass

class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

try:
    from reproducer.models import Picking
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script sets up a Django environment and defines the `Document` and `Picking` models. It then attempts to import the `Picking` model, which should raise an `ImproperlyConfigured` exception if the issue is present. The script uses the provided `print_stacktrace` function to print the stack trace of the exception, and exits with code 1 if the issue is reproduced. If the issue is not reproduced, it prints a success message and exits with code 0.