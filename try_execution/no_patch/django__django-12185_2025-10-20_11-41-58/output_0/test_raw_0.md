```python
# reproducer.py
from django.db import models
from django.db.models import Window, F, Case, When, Value, BooleanField
from django.db.models.functions import Lag
from django.core.exceptions import NotSupportedError
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        "__main__",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)

from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

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
    )
    print("Issue seems fixed, exiting with code 0")
except NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Django raised NotSupportedError when using window expressions in conditional statements in the SELECT clause.")

except Exception as e:
    print_stacktrace(e)
    raise

```

This script is set up to reproduce the described issue where Django raises a `NotSupportedError` when using window expressions in conditional statements only in the SELECT clause. When the issue is present, the script will catch the `NotSupportedError`, print a detailed stack trace showing where the error occurred, and then raise an `AssertionError`. The script requires Django to be installed and expects to be run in an environment where Django is configured to use an SQLite memory database for simplicity.

To run this script, you need to ensure Django is installed in your environment, which you can do by running `pip install Django` if you haven't already. After setting up Django, you can execute the script with `python3 reproducer.py`. If the issue is fixed in your Django version, the script will exit with code 0, indicating no error.