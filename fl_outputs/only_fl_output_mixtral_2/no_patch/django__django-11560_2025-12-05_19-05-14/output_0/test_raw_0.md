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

# Create a MyModel object with a DurationField value
duration_value = timezone.timedelta(days=365*2)  # 2 years
my_obj = MyModel.objects.create(duration=duration_value)

# Try to filter MyModel objects based on the year extracted from the DurationField
try:
    MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("ValueError should not be raised")
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with a stack trace of the issue. The issue is that `ExtractYear` has an optimization where it compares the source date with a range of dates, but this optimization fails when the source is a `DurationField` because intervals are not comparable with dates.

To fix the issue, you can modify the `ExtractYear` function to handle `DurationField` values differently, or you can convert the `DurationField` value to a date value before passing it to `ExtractYear`. For example, you can modify the script as follows:
```python
from django.db.models import DurationField, F, Value
from django.db.models.functions import Cast, DateTimeField, ExtractYear
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

# Create a MyModel object with a DurationField value
duration_value = timezone.timedelta(days=365*2)  # 2 years
my_obj = MyModel.objects.create(duration=duration_value)

# Convert the DurationField value to a date value before passing it to ExtractYear
MyModel.objects.annotate(
    date=Cast('duration', output_field=DateTimeField()),
    year=ExtractYear('date')
).filter(year__gt=1)
```
This modified script should not raise any exceptions and should print the expected queryset.