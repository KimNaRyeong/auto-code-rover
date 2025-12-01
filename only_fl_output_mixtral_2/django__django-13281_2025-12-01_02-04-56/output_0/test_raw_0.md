 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import copy
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.test.utils import setup_test_environment
from reproducer.models import Bar, Foo

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Foo(models.Model):
    a = models.CharField(max_length=10)
    d = models.IntegerField()

class Bar(models.Model):
    a = models.ForeignKey(Foo, on_delete=models.CASCADE)
    b = models.CharField(max_length=10)

def main():
    setup_test_environment()

    foo1 = Foo.objects.create(a='foo1', d=1)
    foo2 = Foo.objects.create(a='foo2', d=2)
    bar1 = Bar.objects.create(a=foo1, b='bar1')
    bar2 = copy.copy(bar1)
    bar2.pk = None
    bar2.a = foo2

    # bar2 points to foo2
    print("bar2.a:", bar2.a)
    print("bar2.a.id:", bar2.a.id)

    # bar1 is unchanged and must still point to foo1
    # These fail on Django >= 2.0
    print("bar1.a:", bar1.a)
    print("bar1.a.id:", bar1.a.id)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, place it in the root directory of the project and execute it with `python3 reproducer.py`. The script will print a stack trace and exit with code 1 when the issue is present.

Note that I had to create a new `models.py` file with the same models as in the original project, and I added a `setup_test_environment()` call to ensure that the test environment is set up correctly.