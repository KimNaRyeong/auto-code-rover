```python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models, IntegrityError
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractBaseUser

# Setup Django environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    AUTH_USER_MODEL='__main__.CustomUser',
)

# Call Django setup
import django
django.setup()


class CustomUser(AbstractBaseUser):
    custom_username = models.CharField(max_length=255)
    USERNAME_FIELD = 'custom_username'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['custom_username'], name='unique_usernames'),
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


def create_superuser(username):
    manage_py = os.path.join(os.path.dirname(django.__file__), 'bin', 'django-admin.py')
    execute_from_command_line([manage_py, 'createsuperuser', '--noinput', '--username', username, '--email', 'test@example.com'])


if __name__ == '__main__':
    # Setup the database and create tables
    execute_from_command_line(['manage.py', 'migrate'])

    username = 'testuser'
    # Create a superuser
    create_superuser(username)

    try:
        # Try to create another superuser with the same username which should raise an error
        create_superuser(username)
        raise AssertionError("An IntegrityError was expected but not raised.")
    except IntegrityError as e:
        print("An IntegrityError was caught as expected.")
        print_stacktrace(e)
        sys.exit(0)
```