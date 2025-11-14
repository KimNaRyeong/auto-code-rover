Here is the corrected standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.db.models import F, Window, Case, When, Value, BooleanField
from django.db.models.functions import Lag

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

class Employee(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    salary = models.IntegerField()

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
    Employee.objects.annotate(
        lag=Window(
            expression=Lag('salary', offset=1),
            partition_by=F('department'),
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True), output_field=BooleanField()
        ),
    ).all()
except NotSupportedError:
    print_stacktrace(e)
    raise AssertionError("Window expression should be allowed in conditional statements used only in the SELECT clause")
```
This script defines a `Employee` model and tries to execute a query that annotates each employee with a lagged salary and a boolean indicating whether the salary has changed. If a `NotSupportedError` is raised during the execution of this query, it prints the stack trace using the provided function and raises an `AssertionError`.