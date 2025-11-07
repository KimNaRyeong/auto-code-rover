Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
from django.db import models
from django.test import TestCase

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

class Reproducer(TestCase):
    def test_create_diamond_mti_common_parents(self):
        try:
            class ItalianRestaurantManyParents(models.Model):
                name = models.CharField(max_length=255)
                address = models.CharField(max_length=255)

                class Meta:
                    abstract = True

            class Supplier(models.Model):
                customers = models.ManyToManyField(ItalianRestaurantManyParents, related_name="provider")

            ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

if __name__ == "__main__":
    Reproducer().test_create_diamond_mti_common_parents()
```

This script creates two model classes, `ItalianRestaurantManyParents` and `Supplier`, with a many-to-many relationship. Then it tries to create an instance of `ItalianRestaurantManyParents`. If the issue is present, it will raise an exception, which we catch and print using our custom `print_stacktrace` function.