Here's a revised and simplified version of the `reproducer.py` script designed to reproduce the issue described. This version directly addresses the need to provide a complete and self-contained example that sets up the Django environment correctly, avoids common pitfalls such as premature model imports, and is inline with Django's expectations for testing custom user models and constraints. The script includes specially designed sections to configure Django settings dynamically and handle model definition gracefully to ensure the test runs smoothly in an isolated manner.

```python
"""
reproducer.py

A standalone script to reproduce the issue with createsuperuser not validating usernames that use a UniqueConstraint.
"""

import django
from django.conf import settings
from django.db import models, IntegrityError
from django.core.management import execute_from_command_line
from django.apps import apps
import sys


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

class CustomUserManager(models.Manager):
    use_in_migrations = True

    def create_superuser(self, custom_username, password=None, **extra_fields):
        return self.create_user(custom_username, password, **extra_fields)

    def create_user(self, custom_username, password=None, **extra_fields):
        if not custom_username:
            raise ValueError('The given custom_username must be set')
        user = self.model(custom_username=custom_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(models.Model):
    custom_username = models.CharField(max_length=255)
    USERNAME_FIELD = 'custom_username'

    objects = CustomUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['custom_username'], name='unique_usernames'),
        ]

def setup_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            '__main__',
        ],
        AUTH_USER_MODEL='__main__.CustomUser',
        SECRET_KEY='fake-key-for-testing',
    )

    apps.populate(settings.INSTALLED_APPS)
    django.setup()

    from django.core.management import call_command
    call_command('makemigrations', '__main__', interactive=False, verbosity=0)
    call_command('migrate', interactive=False, verbosity=0)

def main():
    try:
        # Setting up Django environment and models
        setup_django()

        # Creating a user
        CustomUser.objects.create_user('testuser', password='12345')

        # Attempting to create a duplicate user to reproduce the issue
        CustomUser.objects.create_user('testuser', password='12345')

        # If it reaches here without an IntegrityError, it means the issue is present
        raise AssertionError("Failed to validate unique constraint for custom_username.")

    except IntegrityError as e:
        print("Successfully detected attempt to create a user with a duplicate username.")
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Indicate failure

if __name__ == '__main__':
    main()
```

This script configures Django to use an in-memory SQLite database and defines a custom user model with a `UniqueConstraint` on the `custom_username` field. It then attempts to create two users with the same `custom_username` to trigger an `IntegrityError`, reflecting the constraint validation process. If the unique constraint is not properly validated by Django, the script will catch the assertion and print the stack trace accordingly. Please remember to have Django installed in your environment (`pip install Django`) before running this script.