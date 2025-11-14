Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models.functions import ExtractYear, Trunc
from django.db.models import Q

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

try:
    class MyModel(models.Model):
        duration = models.DurationField()

    result = MyModel.objects.annotate(year=ExtractYear(Trunc('duration', 'day'))).filter(year__gt=1)
except Exception as e:
    print_stacktrace(e)
    raise
```

This script sets the DJANGO_SETTINGS_MODULE environment variable before creating the Django model and attempting to annotate it with an ExtractYear lookup.