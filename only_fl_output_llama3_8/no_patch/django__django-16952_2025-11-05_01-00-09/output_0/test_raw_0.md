Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model_inheritance.settings')
django.setup()

class ItalianRestaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Place(models.Model):
    pass

class Supplier(Place):
    customers = models.ManyToManyField(ItalianRestaurant, related_name="provider")

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

class ModelInheritanceTests(TestCase):

    def test_create_diamond_mti_common_parents(self):
        try:
            ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected exception not raised")

if __name__ == "__main__":
    test_create_diamond_mti_common_parents()
```

This script sets up the models and tries to create an instance of `ItalianRestaurantManyParents`. If the creation fails, it prints the stack trace and raises an `AssertionError` using the provided function.