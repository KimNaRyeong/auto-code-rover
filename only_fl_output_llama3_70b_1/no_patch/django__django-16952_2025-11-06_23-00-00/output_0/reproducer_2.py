import os
import sys

from django.conf import settings
from django.test import TestCase
from django.db import models

settings.configure(
    INSTALLED_APPS=['tests'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}}
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
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'migrate'])
    
    class Place(models.Model):
        name = models.CharField(max_length=50)
        address = models.CharField(max_length=80)
        
    class Restaurant(Place):
        serves_gnocchi = models.BooleanField(default=False)
        
    class ItalianRestaurant(Restaurant):
        pass
        
    class ItalianRestaurantManyParents(ItalianRestaurant, Place):
        pass
    
    from django.db.models.base import ModelBase
    ModelBase.__prepare__(Place)
    ModelBase.__prepare__(Restaurant)
    ModelBase.__prepare__(ItalianRestaurant)
    ModelBase.__prepare__(ItalianRestaurantManyParents)
    
    ItalianRestaurantManyParents.objects.create(
        name="Ristorante Miron",
        address="1234 W. Ash",
    )
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Creating objects with nested MTI crashes")
else:
    sys.exit(0)
