Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

from django.db import models, connection
from django.db.models import Case, When, Value, ExpressionWrapper, F

class Foo(models.Model):
    a = models.CharField(max_length=1)
    d = models.DecimalField(max_digits=1, decimal_places=0)

def test_00compare_field():
    Foo.objects.create(a='', d=1)
    try:
        result = Foo.objects.filter(d__gt=0).get()
        assert result.d > 0
    finally:
        print(connection.queries[-1]['sql'])

def test_01compare_annotation_value_literal():
    Foo.objects.create(a='', d=0)
    try:
        result = Foo.objects.annotate(
            x=Value(1, output_field=models.DecimalField(max_digits=1, decimal_places=0)),
        ).filter(x__gt=0).get()
        assert result.x > 0
    finally:
        print(connection.queries[-1]['sql'])

def test_02compare_annotation_expressionwrapper_literal():
    Foo.objects.create(a='', d=0)
    try:
        result = Foo.objects.annotate(
            x=ExpressionWrapper(
                Value(1),
                output_field=models.DecimalField(max_digits=1, decimal_places=0),
            ),
        ).filter(x__gt=0).get()
        assert result.x > 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Comparing a literal annotation using ExpressionWraper and Value to a literal does not work")

def test_03compare_case_annotation():
    Foo.objects.create(a='', d=1)
    try:
        result = Foo.objects.annotate(
            x=Case(When(a='', then=F('d'))),
        ).filter(x__gt=0).get()
        assert result.x > 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Comparing a Case annotation wrapping a field to a literal does not work")

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

test_00compare_field()
test_01compare_annotation_value_literal()
test_02compare_annotation_expressionwrapper_literal()
test_03compare_case_annotation()
```
<|start_header_id|>