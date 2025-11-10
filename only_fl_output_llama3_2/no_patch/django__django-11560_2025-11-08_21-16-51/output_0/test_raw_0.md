Here is the reproducer script:

```python
import datetime
from django.db import models
from django.db.models.functions import ExtractYear, Trunc
from django.db.models import Q
from django.core.exceptions import AssertionError

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

class MyModel(models.Model):
    duration = models.DurationField()

def main():
    try:
        MyModel.objects.annotate(year=ExtractYear(Trunc('duration', 'day'))).filter(year__gt=1)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script defines a `MyModel` with a `DurationField`, and then attempts to annotate the model with an expression that uses `ExtractYear` on the duration. The `filter` method is used to filter the results, but since durations are not comparable with dates, this should raise an exception.

The script also includes the `print_stacktrace` function as requested, which prints a stack trace of the issue when it occurs.