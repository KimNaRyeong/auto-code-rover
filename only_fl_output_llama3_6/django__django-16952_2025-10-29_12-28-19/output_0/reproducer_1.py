import os
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import AssertionError
from functools import wraps

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

def assert_raises(expected_exception, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except expected_exception as e:
            raise AssertionError("Expected exception not raised") from e
    return wrapper

class Restaurant(models.Model):
    name = models.CharField(max_length=255)

class Place(models.Model):
    address = models.CharField(max_length=255)

class ItalianRestaurant(Restaurant):
    serves_gnocchi = models.BooleanField(default=False)

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

class Supplier(Place):
    customers = models.ManyToManyField(Restaurant, related_name="provider")

class ModelInheritanceTests(TestCase):

    @assert_raises(AssertionError, lambda: ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash"))
    def test_create_diamond_mti_common_parents(self):
        pass

if __name__ == "__main__":
    tests = ModelInheritanceTests()
    try:
        tests.test_create_diamond_mti_common_parents()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
