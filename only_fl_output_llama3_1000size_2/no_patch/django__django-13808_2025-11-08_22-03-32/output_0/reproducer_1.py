import os
from django.conf import settings
from django.db import connections
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_issue():
    settings.configure({
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'OPTIONS': {'service': 'my_alias'}
            }
        }
    })
    
    try:
        connections['default']
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    check_issue()
