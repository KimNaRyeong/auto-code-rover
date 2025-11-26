Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment, teardown_test_environment

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

setup_test_environment()

# Define the models
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

try:
    # Create some instances of the models
    for i in range(5):
        Parent.objects.create()
        Child.objects.create()

    # Query the Child model and check the order
    children = Child.objects.all()
    pks = [child.pk for child in children]
    assert pks == sorted(pks, reverse=True), "Ordering is incorrect"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

teardown_test_environment()

sys.exit(0)
```
This script defines the `Parent` and `Child` models with the specified Meta ordering, creates some instances of these models, queries the `Child` model, and checks if the results are ordered correctly. If the ordering is incorrect, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1. If the issue is fixed, the script exits with code 0.

Note that this script assumes a Django project structure with a `settings.py` file in the root directory. You may need to adjust the `os.environ['DJANGO_SETTINGS_MODULE']` line accordingly.