# reproducer.py

import os
import django
from django.conf import settings

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

def setup_django_environment():
    # Setup minimal necessary settings for Django
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_I18N=True,
        USE_L10N=True,
        SECRET_KEY='django_tests_secret_key',
    )
    django.setup()

def reproduce_issue():
    from django.db.models import Q, Exists
    from django.contrib.auth import get_user_model

    try:
        q = Q(Exists(get_user_model().objects.filter(username='jim')))
        _ = q.deconstruct()  # This line is expected to trigger the TypeError

        # If the script reaches this point, assume the issue does not exist.
        print("No issue detected.")
        sys.exit(0)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue detected.")

if __name__ == "__main__":
    setup_django_environment()

    try:
        reproduce_issue()
    except AssertionError:
        sys.exit(1)
