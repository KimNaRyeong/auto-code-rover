I apologize for the previous mistake. Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db.models import F, Window, Case, When, Value, BooleanField
from django.test import TestCase

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from django.db import models
from django.core.exceptions import NotSupportedError

class Employee(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    salary = models.IntegerField()

try:
    qs = Employee.objects.annotate(
        lag=Window(expression=F('salary'), partition_by=F('department'), order_by=[F('salary').asc(), F('name').asc()])
    ).annotate(
        is_changed=Case(When(salary=F('lag'), then=Value(False)), default=Value(True), output_field=BooleanField())
    )
    qs.query.build_query()
except NotSupportedError as e:
    print_stacktrace(e)
    assert False, "Window expression not allowed in conditional statements used only in the SELECT clause"
else:
    print("Issue is fixed")
```
This script defines a `Employee` model and tries to annotate it with a window expression using `Window` and a conditional statement using `Case`. If a `NotSupportedError` exception is raised, it prints the stack trace using the provided `print_stacktrace` function and asserts that the issue is present. If no exception is raised, it means the issue is fixed and the script exits with code 0.

Note: You need to create a `reproducer` directory with a `settings.py` file containing the Django settings for this script to work.