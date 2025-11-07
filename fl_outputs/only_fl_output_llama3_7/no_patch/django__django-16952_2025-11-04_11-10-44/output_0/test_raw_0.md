Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import django
from django.db import models
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model_inheritance.settings')
django.setup()

class Reproducer(TestCase):
    def test_reproduce_issue(self):
        class Restaurant(models.Model):
            name = models.CharField(max_length=255)

        class Place(Restaurant):
            pass

        class ItalianRestaurant(Place):
            serves_gnocchi = models.BooleanField(default=False)

        class ItalianRestaurantManyParents(ItalianRestaurant, Place):
            pass

        with self.assertRaises(AssertionError):
            ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")

if __name__ == '__main__':
    try:
        Reproducer().test_reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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

This script sets up the necessary models and tries to create an `ItalianRestaurantManyParents` object. If the issue is present, it will raise an `AssertionError`, which will be caught by the script and a stack trace will be printed.