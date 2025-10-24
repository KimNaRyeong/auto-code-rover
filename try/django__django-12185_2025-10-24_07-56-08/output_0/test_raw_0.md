```python
# reproducer.py
from django.db import models
from django.db.models import F, Window, Case, Value, When, BooleanField
from django.db.models.functions import Lag
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer_settings")
django.setup()

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

class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'

def reproduce_issue():
    try:
        Employee.objects.annotate(
            lag=Window(
                expression=Lag(expression='salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True), output_field=BooleanField()
            ),
        )
        print("No issue detected, the script ran successfully.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced successfully.") from e

if __name__ == "__main__":
    reproduce_issue()
```