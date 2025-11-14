Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

from django.db import models

class Buss(models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

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
    Buss.objects.create(jurisdiction='GB', name='Bus1')
    Buss.objects.create(jurisdiction='Universal', name='Bus2')
    Buss.objects.create(jurisdiction='Company', name='Bus3')

    qs = jurisdiction_qs('GB')
    assert qs.count() == 34, "Incorrect count"

    try:
        assert qs.filter(jurisdiction='GB').count() == 8, "Incorrect filtering"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
```
This script creates a few `Buss` objects and then tests the `jurisdiction_qs` function. It asserts that the count of the queryset is correct, and then filters the queryset by jurisdiction 'GB' and asserts that the count is 8. If the assertion fails, it prints the stack trace using the provided `print_stacktrace` function and exits with code 1.

To run this script, create a new Django project and app, and add the `reproducer.py` file to the root directory of the project. Then, run `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print the stack trace.