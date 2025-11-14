Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.db import models
from django.test.utils import override_settings

class Foo(models.Model):
    a = models.CharField(max_length=1)
    d = models.DecimalField(max_digits=1, decimal_places=0)

@override_settings(DEBUG=True)
def test_00compare_field():
    Foo.objects.create(a='', d=1)
    try:
        Foo.objects.filter(d__gt=0).get()
    finally:
        from django.db import connection
        print(connection.queries[-1]['sql'])

@override_settings(DEBUG=True)
def test_01compare_annotation_value_literal():
    Foo.objects.create(a='', d=0)
    try:
        Foo.objects.annotate(
            x=models.Value(1, output_field=models.fields.DecimalField(max_digits=1, decimal_places=0)),
        ).filter(x__gt=0).get()
    finally:
        from django.db import connection
        print(connection.queries[-1]['sql'])

@override_settings(DEBUG=True)
def test_02compare_annotation_expressionwrapper_literal():
    Foo.objects.create(a='', d=0)
    try:
        Foo.objects.annotate(
            x=models.ExpressionWrapper(
                models.Value(1),
                output_field=models.fields.DecimalField(max_digits=1, decimal_places=0),
            ),
        ).filter(x__gt=0).get()
    finally:
        from django.db import connection
        print(connection.queries[-1]['sql'])

@override_settings(DEBUG=True)
def test_03compare_case_annotation():
    Foo.objects.create(a='', d=1)
    try:
        Foo.objects.annotate(
            x=models.Case(models.When(a='', then=models.F('d'))),
        ).filter(x__gt=0).get()
    finally:
        from django.db import connection
        print(connection.queries[-1]['sql'])

def main():
    test_00compare_field()
    test_01compare_annotation_value_literal()
    test_02compare_annotation_expressionwrapper_literal()
    test_03compare_case_annotation()

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

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
```
This script defines the `Foo` model and four test functions that reproduce the issue. The `main` function runs these tests, and if any of them raise an exception, it prints the stack trace using the `print_stacktrace` function and raises an `AssertionError`. If all tests pass without raising an exception, the script exits with code 0.

To run this script, create a new file called `reproducer.py` in the root directory of your Django project, copy-paste the above code into it, and then run it using `python3 reproducer.py`.