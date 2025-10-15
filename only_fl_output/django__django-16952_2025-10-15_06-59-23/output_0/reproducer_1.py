# reproducer.py

import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.apps import apps
from django.db import models

# Setup minimal Django settings
settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        '__main__',  # This script represents the app
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

# Initialize Django to avoid `AppRegistryNotReady` error
apps.populate(settings.INSTALLED_APPS)

# Define models to reproduce the issue
class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)

class ItalianRestaurant(Restaurant):
    serves_gnocchi = models.BooleanField(default=False)

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

class Supplier(Place):
    customers = models.ManyToManyField(Restaurant, related_name="provider")


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


def run_tests():
    # Django needs to be setup before models can be used
    execute_from_command_line(['manage.py', 'migrate'])

    # Attempt to reproduce the given issue
    try:
        ItalianRestaurantManyParents.objects.create(
            name="Ristorante Miron",
            address="1234 W. Ash",
        )
        # If the code reaches this point without exception, the issue did not occur
        print("Issue not reproduced, test passed!")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, AttributeError), "Unexpected exception type"
        print("Issue reproduced successfully.")
        sys.exit(0)


if __name__ == '__main__':
    run_tests()
