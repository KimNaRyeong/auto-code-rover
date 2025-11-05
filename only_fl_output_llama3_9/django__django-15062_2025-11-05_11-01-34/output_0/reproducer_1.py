import os
from django.db import models, connection
from django.test.utils import override_settings
from django.test import TestCase
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

class DecimalFieldTestCase(TestCase):
    @override_settings(DEBUG=True)
    def test_decimal_field(self):
        class Foo(models.Model):
            a = models.CharField(max_length=10)
            d = models.DecimalField(max_digits=1, decimal_places=0)

        foo = Foo.objects.create(a='', d=1)
        try:
            Foo.objects.annotate(x=models.Value(1, output_field=models.fields.DecimalField(max_digits=1, decimal_places=0))).filter(x__gt=0).get()
        except Exception as e:
            print_stacktrace(e)

        queries = connection.queries
        if len(queries) > 0 and 'SELECT' in queries[-1]['sql']:
            print(connection.queries[-1]['sql'])
        else:
            raise AssertionError("Expected a SELECT query")

if __name__ == '__main__':
    try:
        DecimalFieldTestCase()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    if connection.queries:
        for query in connection.queries:
            if 'SELECT' not in query['sql']:
                raise AssertionError("Expected a SELECT query")
    else:
        raise AssertionError("No queries were executed")

    exit(0)
