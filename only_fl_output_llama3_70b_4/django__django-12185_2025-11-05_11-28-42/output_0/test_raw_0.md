Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.db.models import F, Window, Lag, Case, When, Value, BooleanField

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
            expression=Lag(expression='salary', offset=1),
            partition_by=F('department'),
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True), output_field=BooleanField()
        ),
    ).all()
except Exception as e:
    print_stacktrace(e)
    assert False, "Window expression should be allowed in conditional statements used only in the SELECT clause"
```
This script defines a `Employee` model and tries to execute a query that annotates each employee with a lagged salary and a boolean indicating whether the salary has changed. If an exception is raised during the execution of this query, it prints the stack trace using the provided function and asserts that the issue should not be present.

You can run this script by executing `python3 reproducer.py` in the root directory of your Django project.