import os
import sys
from django.conf import settings
from django.test import TestCase
from django.db import models

# Configure Django settings
settings.configure(
    INSTALLED_APPS=['reproducer'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

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

try:
    # Define the models
    class Place(models.Model):
        name = models.CharField(max_length=50)
        address = models.CharField(max_length=80)

    class Restaurant(Place):
        serves_gnocchi = models.BooleanField(default=False)

    class ItalianRestaurant(Restaurant):
        pass

    class ItalianRestaurantManyParents(ItalianRestaurant, Place):
        pass

    # Create the database tables
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'migrate'])

    # Try to create an object with nested MTI
    ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")

except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Creating objects with nested MTI crashes")
