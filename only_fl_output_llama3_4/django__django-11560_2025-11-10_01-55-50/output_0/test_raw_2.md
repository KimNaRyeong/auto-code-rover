Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import ExtractYear, Trunc
import datetime

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
    django.setup()

    class MyModel(models.Model):
        duration = models.DurationField()

    result = MyModel.objects.annotate(year=ExtractYear(Trunc('duration', 'day'))).filter(year__gt=1)
    
    if result.count() != 0:
        raise AssertionError("Issue not reproduced")
except Exception as e:
    print_stacktrace(e)
finally:
    exit(0)
```

This script sets up a Django environment, defines a model with a DurationField, and then attempts to filter the results based on an annotated field. If the issue is present (i.e., if the query returns any results), it raises an AssertionError.