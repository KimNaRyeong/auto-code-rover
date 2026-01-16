Based on your specification, here's a standalone Python file, named `reproducer.py`, designed to explicitly reproduce the issue with using `.distinct()` following a `.union()` on annotated Django querysets. If the issue persists, it should raise an `AssertionError` indicating the problem, along with a clear stack trace to show where the issue originates in the script.

Please ensure that this script is adjusted to fit into your Django project setup, specifically regarding models and user creation. Modify the `DATABASES` settings if you're not using SQLite. Ensure Django is initialised correctly if this script is run outside of a standard Django project structure.

```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models import Value, IntegerField


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


# Minimal Django Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define your models here
class User(models.Model):
    name = models.CharField(max_length=255)

class Sample(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Run the script to reproduce the issue
def main():
    # Your testing logic here. Make sure to catch the AssertionError and print the stack trace.
    try:
        # Assuming this function populates the database with necessary initial data
        user = User.objects.create(name="Test User")
        Sample.objects.create(user=user, name="Sam1")
        Sample.objects.create(user=user, name="Sam2 acid")
        Sample.objects.create(user=user, name="Sam3")
        Sample.objects.create(user=user, name="Sam4 acid")
        Sample.objects.create(user=user, name="Dub")
        Sample.objects.create(user=user, name="Dub")
        Sample.objects.create(user=user, name="Dub")

        qs1 = Sample.objects.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = Sample.objects.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))

        qs = qs1.union(qs2).order_by('name').distinct('name')

        if qs.count() != 2:
            raise AssertionError("Expected exactly 2 distinct entries after union.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exits with error code when exception is caught

    sys.exit(0)  # Exits with success code if the test passes without exceptions

if __name__ == '__main__':
    main()
```

Make sure you have Django installed in your environment, and adjust the `User` and `Sample` model definitions according to your project schema. Execute the script with `python3 reproducer.py` from the root directory of your Django project. This will attempt to reproduce the described issue, and in the event of an exception or error, it will print a stack trace for debugging purposes.