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

try:
    from django.db import models
    class Restaurant(models.Model):
        name = models.CharField(max_length=255)

    class Place(Restaurant):
        pass

    class ItalianRestaurant(Place):
        serves_gnocchi = models.BooleanField(default=False)

    class ItalianRestaurantManyParents(ItalianRestaurant, Place):
        pass

    class Supplier(Place):
        customers = models.ManyToManyField(Restaurant, related_name="provider")

    ItalianRestaurantManyParents.objects.create(name="Ristorante Miron", address="1234 W. Ash")
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected exception not raised"
