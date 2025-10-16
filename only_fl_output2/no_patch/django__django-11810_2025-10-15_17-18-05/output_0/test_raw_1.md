```python
# reproducer.py
import django
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

# Define a minimal Django configuration to reproduce the issue
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ":memory:",
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script acts as a standalone Django app
    ],
)

django.setup()


# Define models according to the issue description
class ModelA(models.Model):
    pass


class ModelB(models.Model):
    pass


class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)


models.Model.check()

# Utility function to print stack trace for the exception
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        print(f'  File "{frame.filename}", line {frame.lineno}', file=sys.stderr)
        print(f"    {frame.line}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


# Reproduce the issue
def reproduce_issue():
    query_1 = ModelC.objects.select_related('model_a')
    print('QUERY 1 before mutation:', str(query_1.query))

    query_2 = query_1.select_related('model_b')
    print('QUERY 2:', str(query_2.query))

    print('QUERY 1 after mutation:', str(query_1.query))

    # Assert that original QuerySet is not mutated, which raises AssertionError if the issue is present
    assert str(query_1.query) != str(query_2.query), "Original QuerySet was mutated!"


if __name__ == '__main__':
    try:
        reproduce_issue()
        print("No issue detected: the original QuerySet was not mutated.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a minimal Django environment, defines the necessary models, and reproduces the issue as described. If the issue **"Chaining select_related mutates original QuerySet"** is still present, it will raise an `AssertionError` and print a detailed stack trace. If the mutation does not occur (meaning the issue is fixed), it prints a confirmation message and exits gracefully.