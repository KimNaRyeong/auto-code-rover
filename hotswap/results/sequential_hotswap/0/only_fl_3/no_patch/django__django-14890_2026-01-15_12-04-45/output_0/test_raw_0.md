```python
import os
import django
from django.conf import settings
from django.db import models

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'testdb',
            }
        },
        INSTALLED_APPS=(
            '__main__',  # This tricks Django into thinking this is a real app
        ),
        USE_TZ=True,
    )
    django.setup()

# Define a custom exception to raise when the issue is detected
class OperatorIssueException(Exception):
    pass

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

def test_query():
    class MyModel(models.Model):
        name = models.CharField(max_length=100)

    # Dynamically create the table for MyModel
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(MyModel)

    # Create data
    for name in ['a', 'b', 'c']:
        MyModel.objects.create(name=name)

    # Perform query operations
    group1 = MyModel.objects.filter(name='a')
    group2 = MyModel.objects.filter(name='b')
    group3 = MyModel.objects.filter(name='c')
    combined_group = group1.union(group2)
    group_and = combined_group & group1
    group_or = combined_group | group3

    # Check if the issue exists and raise an exception if so
    try:
        if str(combined_group.query) == str(group_and.query) == str(group_or.query):
            raise OperatorIssueException('Operator "&" and "|" are silently ignored after QuerySet.union(),'
                                         ' intersection(), and difference().')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        setup_django_environment()
        test_query()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except OperatorIssueException as e:
        print_stacktrace(e)
        raise
    else:
        print("No issue detected.")

```
This script sets up a minimal Django environment, defines a model, and executes queries that should trigger the issue if "&" and "|" operators are silently ignored after `QuerySet.union()`, with error handling to print a detailed stack trace on failure. Note that for this script to work outside a standard Django project, it hacks around Django's system checks by setting up the environment and database connection in a non-standard way, specifically for demonstration purposes.