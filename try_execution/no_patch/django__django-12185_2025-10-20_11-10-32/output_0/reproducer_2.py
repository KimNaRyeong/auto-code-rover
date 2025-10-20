import django
from django.conf import settings
from django.db import models, OperationalError, ProgrammingError
from django.db.models import F, Window, Case, When, Value, BooleanField
from django.db.models.functions import Lag

# Function to print stack trace for exceptions
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

# Dynamically configure Django settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            '__main__',  # This script acts as a standalone Django app
        ],
        USE_TZ=True,
    )

django.setup()

# Define a simple Employee model for this test
class Employee(models.Model):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'  # Makes this model belong to the standalone script app

try:
    # Attempt to use a window expression in a Case When statement within the annotate query
    result = Employee.objects.annotate(
        lag=Window(
            expression=Lag('salary', offset=1),
            partition_by=[F('department')],
            order_by=[F('salary').asc(), F('name').asc()],
        ),
        is_changed=Case(
            When(salary=F('lag'), then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        ),
    )
    list(result)  # Force query evaluation to potentially trigger the error
    print("Test passed: Error was not raised, the issue might be fixed.")
    exit(0)

except (OperationalError, ProgrammingError) as e:
    # Print the stack trace for the database operation exception
    print_stacktrace(e)
    assert False, "Issue reproduced: Not allowed to use window expressions in this context."

except Exception as e:
    # If any other exception is raised, print its stack trace
    print_stacktrace(e)
    assert False, "An unexpected error occurred."
