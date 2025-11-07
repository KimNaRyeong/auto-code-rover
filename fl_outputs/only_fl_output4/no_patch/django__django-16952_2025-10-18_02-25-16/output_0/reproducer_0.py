# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.test import TestCase

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This module (reproducer.py) contains the defined models and tests.
    ),
    USE_TZ=True,
)
django.setup()

# Define models to replicate the issue
class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

class ItalianRestaurant(Restaurant):
    serves_gnocchi = models.BooleanField(default=False)

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

class Supplier(Place):
    customers = models.ManyToManyField(Restaurant, related_name="provider")

# Test case replicating the issue
class ModelInheritanceTest(TestCase):
    def test_create_diamond_mti_common_parents(self):
        try:
            ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")
            assert False, "This should have raised an exception"
        except Exception as e:
            print_stacktrace(e)
            assert isinstance(e, AttributeError), "The exception type should be AttributeError"

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

if __name__ == "__main__":
    import django.core.management
    from django.core.management.commands.flush import Command as FlushCommand

    # Prepare the database
    django.core.management.call_command("migrate", verbosity=0)
    django.core.management.call_command(FlushCommand(), verbosity=0, interactive=False)
    
    # Run the test
    t = ModelInheritanceTest()
    t.test_create_diamond_mti_common_parents()
