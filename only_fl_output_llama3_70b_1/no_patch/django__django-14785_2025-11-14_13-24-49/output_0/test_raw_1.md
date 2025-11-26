Here is the `reproducer.py` script to reproduce the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment

# Create a new Django project and app
os.system("django-admin startproject nanbug")
os.chdir("nanbug")
os.system("python manage.py startapp myapp")

# Define the model with DecimalField
with open("myapp/models.py", "w") as f:
    f.write("""
from django.db import models

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)
""")

# Create and apply migrations
os.system("python manage.py makemigrations myapp")
os.system("python manage.py migrate")

# Set up the test environment
setup_test_environment()

from django.test import TestCase
from myapp.models import MyModel

class ReproducerTestCase(TestCase):
    def test_nan_issue(self):
        obj = MyModel.objects.create(value=float('nan'))
        try:
            obj.refresh_from_db()
            self.fail("Expected TypeError, but no exception was raised")
        except TypeError as e:
            print_stacktrace(e)
            raise AssertionError("Issue is present")

if __name__ == "__main__":
    ReproducerTestCase().test_nan_issue()

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
```
This script creates a new Django project and app, defines a model with a DecimalField, creates and applies migrations, and then runs a test case that reproduces the issue. If the issue is present, it raises an AssertionError and prints the stack trace of the TypeError exception.