import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer_settings")
import django
from django.conf import settings
from django.db import models, NotSupportedError, connection
from django.db.models import F, Window, Case, When, Value, BooleanField

# Ensure correct imports for window function expressions
from django.db.models.functions import Lag

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup():
    # Define minimal Django settings required for the script to run
    minimal_settings = {
        'INSTALLED_APPS': ['__main__'],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',  # Use django.db.backends.postgresql for PostgreSQL
                'NAME': ':memory:',
            }
        },
        'USE_TZ': True,
    }
    settings.configure(**minimal_settings)
    django.setup()

    # Define a simple Employee model
    class Employee(models.Model):
        name = models.CharField(max_length=100)
        salary = models.DecimalField(max_digits=10, decimal_places=2)
        department = models.CharField(max_length=100)

        class Meta:
            app_label = '__main__'

    # Dynamically create the model tables
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Employee)

    return Employee

def main():
    Employee = setup()

    try:
        query = Employee.objects.annotate(
            lag=Window(
                expression=Lag('salary', offset=1),
                partition_by=[F('department')],
                order_by=['salary', 'name']
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True),
                output_field=BooleanField()
            ),
        )

        # Force query to execute by evaluating its result
        list(query)

        print("The issue is not present.")
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Window expressions are not allowed in conditional statements in the SELECT clause.")

if __name__ == "__main__":
    main()
