# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

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

if not settings.configured:
    settings.configure(
        SECRET_KEY='a-very-secret-key',
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            '__main__',  # This app is needed to let Django know where to find the models
        ),
        USE_TZ=True,
    )

django.setup()

# Models definition (should be after django.setup())
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

# Reproducing the issue after setting up models and migrations.
def reproduce():
    call_command('migrate')
    
    try:
        ItalianRestaurantManyParents.objects.create(
            name="Ristorante Miron",
            address="1234 W. Ash",
        )
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    reproduce()
