import os
from django.db import connections
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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

def reproduce_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImproperlyConfigured as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
    return wrapper

@reproduce_issue
def test_issue():
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'OPTIONS': {'service': 'my_alias'}
        }
    }

if __name__ == "__main__":
    test_issue()
