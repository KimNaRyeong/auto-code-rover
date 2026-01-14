 Here is a standalone Python script `reproducer.py` that reproduces the given issue:
```python
import sys
import traceback
from django.core.management import execute_from_command_line
from django.db import connection

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    # Define the models
    class Bar(object):
        pass

    class Foo(object):
        bar = models.ManyToManyField('Bar', blank=True)

    # Create the models
    models.ModelBase.register(Bar)
    models.ModelBase.register(Foo)

    # Create the initial migration
    execute_from_command_line(["manage.py", "makemigrations", "app"])

    # Apply the initial migration
    execute_from_command_line(["manage.py", "migrate"])

    # Change the ManyToManyField to target 'Foo' instead of 'Bar'
    class Bar(object):
        pass

    class Foo(object):
        bar = models.ManyToManyField('Foo', blank=True)

    # Create the new migration
    execute_from_command_line(["manage.py", "makemigrations", "app"])

    # Apply the new migration
    execute_from_command_line(["manage.py", "migrate"])

    # Save a new 'Foo' instance
    cursor = connection.cursor()
    cursor.execute("INSERT INTO app_foo (id, bar_id) VALUES (1, NULL)")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
To run the script, save it to a file named `reproducer.py` in the root directory of your Django project, and then execute it with the command `python3 reproducer.py`. If the issue is present, the script will print a stack trace and exit with code 1. If the issue is fixed, the script will exit with code 0.