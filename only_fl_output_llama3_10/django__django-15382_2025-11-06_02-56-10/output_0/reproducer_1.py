import os
from django.db import models
from django.db.models import Q, Exists
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

def main():
    class MyModel(models.Model):
        name = models.CharField(max_length=255)

    qs = MyModel.objects.filter(~Q(name='test'), ~models.Exists(MyModel.objects.none()))
    if not str(qs.query).startswith('SELECT'):
        raise AssertionError("WHERE block is missing")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

