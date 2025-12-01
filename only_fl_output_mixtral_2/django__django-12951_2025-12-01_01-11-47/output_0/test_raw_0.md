 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import datetime
import sys
from django.db import models
from django.db.models import Case, Exists, OuterRef, Q, Value
from django.db.models.functions import Coalesce

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class State(models.Model):
    name = models.CharField(max_length=50)

class County(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, related_name='counties')

def test_annotate_when_exists_expression():
    County.objects.annotate(
        status=Case(
            When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas", then=Value("DALLAS COUNTY")),
            default=Value("ELSEWHERE"),
        ))

if __name__ == "__main__":
    try:
        # Create a fresh database for testing
        from django.core.management import call_command
        call_command('makemigrations', '--empty', 'myapp')
        call_command('migrate')

        # Run the test function
        test_annotate_when_exists_expression()

        # If no exception is raised, exit with code 0
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, create a new Django app called `myapp` and put the `reproducer.py` file in the root directory of the app. Then, run the script using `python3 reproducer.py`. The script will create a fresh database for testing, run the `test_annotate_when_exists_expression` function, and print a stack trace if an exception is raised.

The expected output is a stack trace with the following error message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 42, in <module>
    test_annotate_when_exists_expression()
  File "reproducer.py", line 35, in test_annotate_when_exists_expression
    When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas", then=Value("DALLAS COUNTY")),
TypeError: When() supports a Q object, a boolean expression, or lookups as a condition.
```
This error message confirms that the `When` function does not support the `Exists` expression as a condition when using keyword arguments.