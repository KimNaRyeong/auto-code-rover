import os
from django.db import models, connection
from django.test.utils import override_settings
from django.core.exceptions import AssertionError

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

@override_settings(DEBUG=True)
def test_decimal_field_reproducer():
    class Foo(models.Model):
        a = models.CharField(max_length=10)
        d = models.DecimalField(max_digits=1, decimal_places=0)

    try:
        Foo.objects.create(a='', d=1)
        query = Foo.objects.annotate(
            x=models.ExpressionWrapper(models.Value(1), output_field=models.fields.DecimalField(max_digits=1, decimal_places=0))
        ).filter(x__gt=0).get()
    except models.DoesNotExist as e:
        print_stacktrace(e)
        raise AssertionError("Expected Foo matching query does not exist.")

if __name__ == "__main__":
    test_decimal_field_reproducer()
