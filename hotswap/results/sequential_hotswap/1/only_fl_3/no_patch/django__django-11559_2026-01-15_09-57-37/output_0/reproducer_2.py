import os
import django
from django.conf import settings
from django.db import models


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


# Configure Django in a minimal setup suitable for running standalone scripts.
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=(
        "__main__",  # This script acts as a standalone Django app.
    ),
    SECRET_KEY="fake-key",
)

django.setup()

# Define models inline with the issue.
class Parent(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = [models.F('name').asc()]  # The usage of F() here causes the issue.

class Child(Parent):
    pass

try:
    # Simulate the faulty behavior mentioned in the description.
    Child.objects.create(name='Child 1')
    children = Child.objects.all()

    # If execution reaches this point without error, the issue did not occur as expected.
    print("Error: The issue could not be reproduced.")
    sys.exit(1)  # Exit with code 1 indicating failure to reproduce.

except Exception as e:
    print_stacktrace(e)
    assert "Cannot resolve keyword 'name'" in str(e), "Unexpected error message."
    sys.exit(0)  # Exit with code 0 indicating successful reproduction.


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    try:
        django.setup()  # Ensure Django is setup again in case of direct execution.
        main()
    except Exception as e:
        print_stacktrace(e)
