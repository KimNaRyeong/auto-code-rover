Here is the reproducer script:

```python
import datetime
from django.db import models
from django.db.models.functions import ExtractYear
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

try:
    settings.configure()
    from django.db import models
    class MyModel(models.Model):
        duration = models.DurationField()

    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    duration = models.DurationField(value=start_date - end_date)

    MyModel(duration=duration).annotate(year=ExtractYear('duration')).filter(year__gt=1)
except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will create a `MyModel` with a `DurationField`, then attempt to annotate and filter the model using `ExtractYear`. If the issue is present, it should raise an exception and print the stack trace.