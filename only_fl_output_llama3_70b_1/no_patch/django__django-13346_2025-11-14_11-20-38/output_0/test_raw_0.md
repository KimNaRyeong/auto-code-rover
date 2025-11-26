Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.test import TestCase

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class JSONField(models.Field):
    pass

class OurModel(models.Model):
    our_field = JSONField()

def setup_test_db():
    from django.test.utils import setup_test_database
    setup_test_database(verbosity=0, interactive=False)

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import reproducer.settings
    setup_test_db()
    
    OurModel.objects.create(our_field={'key': 0})
    OurModel.objects.create(our_field={'key': 1})

    first_filter = {'our_field__key__in': [0]}
    second_filter = {'our_field__key': 0}

    try:
        first_items = OurModel.objects.filter(**first_filter)
        second_items = OurModel.objects.filter(**second_filter)

        assert len(first_items) == len(second_items), "Length of querysets are not equal"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script creates a test database, defines a model with a JSONField, and then tries to filter the model using both `__in` lookup and exact match. If the lengths of the resulting querysets are not equal, it raises an AssertionError, prints the stack trace, and exits with code 1.

To run this script, create a new file called `reproducer.py` in the root directory of your project, copy the above code into it, and then execute it using `python3 reproducer.py`.