Here is the reproducer script:

```python
import datetime
from django.db import models
from django.db.models.functions import ExtractYear
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

try:
    class MyModel(models.Model):
        duration = models.DurationField()

    result = MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=datetime.date(2020, 1, 1))
    assert False, "Expected ValueError"
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an AssertionError and print a stack trace.