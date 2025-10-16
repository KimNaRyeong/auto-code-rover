import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line

# Setup minimal Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    BASE_DIR=BASE_DIR,
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script as an app
    ),
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',  # Resolve system check warning
)

django.setup()

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

class ItalianRestaurant(Restaurant):
    serves_gnocchi = models.BooleanField(default=False)

class ItalianRestaurantManyParents(ItalianRestaurant, Place):
    pass

# Define a function to print the detailed stack trace when exceptions occur
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

# Function to reproduce the issue and print a stack trace if it occurs
def reproduce_issue():
    try:
        # Attempt to create an instance that leads to the reported crash
        ItalianRestaurantManyParents.objects.create(
            name="Test Ristorante",
            address="123 Test Ave"
        )
        # Expected failure point
        print("The script did not encounter the expected issue.")
    except Exception as e:
        print_stacktrace(e)
        # Raise assertion error if the specific issue is caught
        assert isinstance(e, AttributeError), "The script encountered an unexpected exception type."

if __name__ == "__main__":
    # Apply migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Reproduce the issue
    reproduce_issue()
