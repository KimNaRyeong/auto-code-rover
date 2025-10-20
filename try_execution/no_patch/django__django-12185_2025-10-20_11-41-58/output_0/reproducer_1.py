# reproducer.py
import django
from django.conf import settings
from django.db import models, OperationalError
from django.db.models import F, Case, Value, Window, When, BooleanField
from django.db.models.functions import Lag

settings.configure(
    INSTALLED_APPS=["__main__"],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    },
    USE_TZ=True,
)

django.setup()

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
    ).first()  # Trigger the query execution to catch any errors
    
    print("The issue seems fixed.")
except Exception as e:  # Catch a broader range of exceptions due to backend specific errors.
    print_stacktrace(e)
    raise AssertionError("Failed to execute window function in SELECT clause.")

