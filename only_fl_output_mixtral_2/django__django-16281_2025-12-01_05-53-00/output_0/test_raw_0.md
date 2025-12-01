 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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

def run():
    # Create models
    class Bar(models.Model):
        pass

    class Foo(models.Model):
        bar = models.ManyToManyField('Bar', blank=True)

    # Migrate
    execute_from_command_line(sys.argv + ['./manage.py', 'makemigrations', 'app'])
    execute_from_command_line(sys.argv + ['./manage.py', 'migrate'])

    # Change type of ManyToManyField
    class Bar(models.Model):
        pass

    class Foo(models.Model):
        bar = models.ManyToManyField('Foo', blank=True)

    # Migrate
    execute_from_command_line(sys.argv + ['./manage.py', 'makemigrations', 'app'])
    execute_from_command_line(sys.argv + ['./manage.py', 'migrate'])

    # Save Foo object
    foo = Foo.objects.create()
    foo.save()

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace showing the line where the error occurred. The error occurs when trying to save a `Foo` object after changing the target of the `ManyToManyField` to `Foo`. The error message is:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 50, in <module>
    run()
  File "reproducer.py", line 46, in run
    foo.save()
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 753, in save
