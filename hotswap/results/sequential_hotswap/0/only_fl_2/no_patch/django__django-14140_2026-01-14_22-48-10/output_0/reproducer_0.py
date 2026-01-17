from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Exists
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

import django
django.setup()

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

def main():
    try:
        query = Q(Exists(get_user_model().objects.filter(username='jim')))
        query.deconstruct()
        # If the query deconstructs without raising an exception, the issue is assumed to be fixed.
        print("Issue appears to be fixed.")
    except Exception as e:
        # If an exception is encountered, it means the issue is still present.
        print_stacktrace(e)
        raise AssertionError("The issue is still present.")

if __name__ == '__main__':
    main()
