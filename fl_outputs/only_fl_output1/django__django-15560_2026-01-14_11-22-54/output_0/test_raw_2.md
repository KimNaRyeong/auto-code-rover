Certainly, for a standalone script tightly focused on this Django issue and fitting within the constraints described, we should establish a minimal Django environment programmatically. This entails setting up a minimal in-memory Django project within the script, including the custom user model and testing the `createsuperuser` process with the described unique constraint scenario.

The following `reproducer.py` script is designed to be self-contained, simulating a Django environment and reproducing the issue without requiring a pre-existing Django project setup. Note, due to this approach, certain elements like `django.setup()` and dynamic model creation are utilized, differing from standard practice but necessary for the isolated scope of this reproduction script.

```python
"""
reproducer.py
-------------

A self-contained script to reproduce the Django `createsuperuser` issue with unique constraints.
"""

import os
import sys

# Setting up a minimal Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
sys.modules['__main__'] = sys.modules[__name__]

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'reproducer',
)
AUTH_USER_MODEL = 'reproducer.CustomUser'

SECRET_KEY = 'fake-key'

from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.db import models
from django.apps import AppConfig

class ReproducerConfig(AppConfig):
    name = 'reproducer'
    verbose_name = "Reproducer App"

# Define a custom user model as described in the issue.
class CustomUser(models.Model):
    custom_username = models.CharField(max_length=255)
    USERNAME_FIELD = 'custom_username'

    class Meta:
        app_label = 'reproducer'
        constraints = [
            models.UniqueConstraint(fields=['custom_username'], name='unique_usernames'),
        ]

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

def main():
    # Simulating Django environment setup
    import django
    from django.core.management.commands.migrate import Command as MigrateCommand

    django.setup()
    MigrateCommand().handle(interactive=False, verbosity=0)

    # Attempt to replicate the issue
    from django.contrib.auth import get_user_model
    CustomUserModel = get_user_model()

    username = "testuser"
    try:
        # First user creation should succeed.
        CustomUserModel.objects.create_superuser(username=username, password="test", email="test@test.com")
        
        # Second user creation with the same username should raise an IntegrityError
        CustomUserModel.objects.create_superuser(username=username, password="test2", email="test2@test.com")
        
        # If this point is reached, it means unique constraints were not properly checked
        raise AssertionError("UniqueConstraint on username did not prevent duplicate superuser creation.")
    except models.IntegrityError as e:
        print("IntegrityError was correctly raised, indicating the unique constraint was violated as expected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exiting with error if any other exception is caught
    else:
        print("Reproduced the issue successfully. Exiting with code 0.")
        exit(0)

urlpatterns = []

if __name__ == '__main__':
    main()
```

This script operates by:

1. Configuring a minimal Django environment programmatically, including in-memory database settings.
2. Defining a custom user model with the unique constraint outlined.
3. Attempting to create two users with the same `custom_username` to trigger an `IntegrityError`, expected due to the unique constraint violation.
4. If an `IntegrityError` is raised on the second user creation attempt, it indicates the unique constraint works as expected. Any other outcome (like creating the user successfully or raising a different type of error) would signal an issue.

Please note, this script is quite unconventional and tailored for a very specific task. Running it in a typical Django project atmosphere or as part of a different Django app setup may require adjustments.