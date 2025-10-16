```python
# reproducer.py
from django.db import models
from django.db.models import F, Value, Window, When, Case
from django.db.models.functions import Lag
from django.core.exceptions import NotSupportedError
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__project__.settings")
django.setup()


class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)


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


def main():
    try:
        Employee.objects.annotate(
            lag=Window(
                expression=Lag(expression='salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True), output_field=models.BooleanField()
            ),
        ).first()
    except NotSupportedError as e:
        print("Issue reproduced successfully.")
        print_stacktrace(e)
        assert True  # The assertion to indicate the presence of the issue
        return
    except Exception as e:
        print("Unexpected exception type.")
        print_stacktrace(e)
        assert False  # This should not happen if the issue is as expected

    # Reaching here means the issue has been fixed and no NotSupportedError was raised.
    print("No issue detected. It seems like the problem has been resolved.")
    assert False  # The script should not reach this point if the issue exists


if __name__ == "__main__":
    main()
```