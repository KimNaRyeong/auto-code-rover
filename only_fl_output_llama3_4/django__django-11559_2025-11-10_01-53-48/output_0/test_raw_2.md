Here is the reproducer script:

```python
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

import os
from django.db import models

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from django.conf import settings

class ParentModel(models.Model):
    class Meta:
        ordering = ['expression']

class ChildModel(ParentModel):
    pass

if __name__ == "__main__":
    try:
        ParentModel.objects.order_by('expression')
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script sets the DJANGO_SETTINGS_MODULE environment variable before importing any Django models. This should allow the script to reproduce the issue.