Here is the reproducer script:

```python
import datetime
from django.db import models
from django.db.models.functions import ExtractYear, Trunc

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

    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)

    data = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days)]

    MyModel.objects.bulk_create([MyModel(duration=datetime.timedelta(days=i)) for i in range((end_date - start_date).days)])

    result = MyModel.objects.annotate(year=ExtractYear(Trunc('duration', 'day'))).filter(year__gt=1)

    if result.count() != 0:
        raise AssertionError("Issue not reproduced")
except Exception as e:
    print_stacktrace(e)
finally:
    exit(0)
```

This script creates a Django model with a DurationField, populates the database with data, and then attempts to filter the results based on an annotated field. If the issue is present (i.e., if the query returns any results), it raises an AssertionError.