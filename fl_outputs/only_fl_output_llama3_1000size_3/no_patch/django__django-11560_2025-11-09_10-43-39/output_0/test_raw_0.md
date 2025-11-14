Here is the reproducer script:

```python
import datetime
from django.db import models
from django.db.models.functions import ExtractYear, Trunc
from django.db.models.expressions import F

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

def reproduce_issue():
    class MyModel(models.Model):
        duration = models.DurationField()

    try:
        MyModel.objects.annotate(year=ExtractYear(Trunc('duration', 'day'))).filter(year__gt=1)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a simple Django model with a DurationField, then attempts to annotate the model with an ExtractYear function and filter on the result. If the issue is present, it will catch the exception, print the stack trace using the provided `print_stacktrace` function, and then re-raise the exception.