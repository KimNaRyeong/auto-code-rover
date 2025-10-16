```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

# Define your Django application settings
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(os.getcwd(), "db.sqlite3"),
        }
    },
    INSTALLED_APPS=("__main__",),
    USE_TZ=True,  # Required for Django 4.0+
)

django.setup()


# Define your models
class ModelA(models.Model):
    name = models.CharField(max_length=255)


class ModelB(models.Model):
    name = models.CharField(max_length=255)


class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)

# Migrate models
from django.core.management import call_command
call_command("makemigrations", "__main__")
call_command("migrate")


# Utility function to print stack trace for the exception
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    Line {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_mutation_issue():
    query_1 = ModelC.objects.select_related('model_a')
    initial_query_str = str(query_1.query)
    print('Initial QUERY 1:', initial_query_str)

    query_2 = query_1.select_related('model_b')
    mutated_query_str = str(query_1.query)
    print('Mutated QUERY 1:', mutated_query_str)

    # Assert if the initial query has been mutated
    assert initial_query_str != mutated_query_str, "The original QuerySet was mutated!"

try:
    test_mutation_issue()
except AssertionError as e:
    print_stacktrace(e)
    raise  # Reraise the assertion to trigger exit code 1 for demonstration purpose
else:
    print("Test passed: The original QuerySet was not mutated.")
    exit(0)  # Exit code 0 to indicate success/no issue
```

This script performs the necessary setup for a Django environment within the script itself, creates the models needed to reproduce the query mutation issue, and provides a function `test_mutation_issue()` to test for the behavior. The test applies `select_related` to a `QuerySet` to check if the original `QuerySet` is mutated after applying an additional `select_related` call. If the issue occurs, it raises an `AssertionError`, and the utility function `print_stacktrace()` prints the stack trace for the exception, giving precise information about where the error happened. If the mutation does not occur, it signifies the absence of the issue, and the script exits with code 0, marking success.