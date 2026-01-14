 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import DurationField, F, Value
from django.db.models.functions import ExtractYear
from django.utils import timezone

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
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
except ValueError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
else:
    print("No exception raised, the issue is fixed.")
    sys.exit(0)
```
When executed with `python3 reproducer.py`, this script should print a stack trace of the `ValueError` exception, which is raised due to the issue with the `ExtractYear` lookup on a `DurationField`. The line numbers of the statements in the stack trace may vary depending on the location of the script in the project directory.

Note that the script uses the `print_stacktrace` function provided in the issue description to print the stack trace with line numbers. The script also exits with code 0 when the issue is fixed, i.e., when no exception is raised.