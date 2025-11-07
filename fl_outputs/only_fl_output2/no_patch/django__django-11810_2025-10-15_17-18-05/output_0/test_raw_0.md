```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models, connection


# Define a minimal Django settings configuration for running the reproducer
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script will act as a standalone Django app
    ],
    USE_TZ=True,
)

django.setup()


# Define the models according to the issue description
class ModelA(models.Model):
    pass


class ModelB(models.Model):
    pass


class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)


# Create the tables for our models in the in-memory database
with connection.schema_editor() as schema_editor:
    schema_editor.create_model(ModelA)
    schema_editor.create_model(ModelB)
    schema_editor.create_model(ModelC)


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


def test_mutate_queryset():
    try:
        query_1 = ModelC.objects.select_related('model_a')
        original_query_str = str(query_1.query)

        query_2 = query_1.select_related('model_b')
        new_query_str = str(query_2.query)

        # Re-check the original query string to verify it hasn't mutated
        assert original_query_str == str(query_1.query), "Original QuerySet was mutated!"

        print("Test passed: Chaining 'select_related' does not mutate original QuerySet.")
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    try:
        test_mutate_queryset()
    except AssertionError:
        os._exit(1)
    os._exit(0)
```

This `reproducer.py` script sets up a minimal Django environment with an in-memory SQLite database, replicates the described issue, and utilizes the provided function to print the stack trace in case an `AssertionError` is raised, indicating the original `QuerySet` was indeed mutated after applying `select_related` a second time. If the issue is fixed and the assertion does not fail, it will print "Test passed" and exit with code `0`.
