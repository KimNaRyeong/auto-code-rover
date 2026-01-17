 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import DurationField, F, Value
from django.db.models.functions import ExtractYear
from django.core.exceptions import ValidationError

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    duration = models.DurationField()

try:
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=Value(1, output_field=DurationField()))
except ValidationError as e:
    print_stacktrace(e)
    sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

raise AssertionError("ValidationError was not raised")
```
When executed with `python3 reproducer.py`, it will print a stack trace of the `ValidationError` that is raised when the issue is present, and exit with code 0. If the issue is fixed, the script will raise an `AssertionError` and exit with code 1.