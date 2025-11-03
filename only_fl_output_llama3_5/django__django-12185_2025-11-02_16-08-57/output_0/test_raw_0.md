Here is the reproducer script:

```python
import django
from django.db.models import Case, When, Value, BooleanField
from django.db.models.expressions import Window, Lag
from django.db.models.functions import F

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
    from django.db.models import NotSupportedError

    class Employee(django.db.models.Model):
        salary = django.db.models.IntegerField()
        name = django.db.models.CharField(max_length=255)
        department = django.db.models.CharField(max_length=255)

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
except NotSupportedError as e:
    print_stacktrace(e)
    raise SystemExit(0)

print("Issue not reproduced")
```

This script will attempt to reproduce the issue by creating a Django model and using window expressions in a conditional statement. If the issue is present, it will catch the `NotSupportedError` exception, print the stack trace, and exit with code 0.