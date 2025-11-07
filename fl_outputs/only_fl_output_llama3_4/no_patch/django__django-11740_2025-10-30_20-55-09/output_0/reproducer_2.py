import os
import django
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.management.commands.makemigrations import CommandError
from django.core.exceptions import ImproperlyConfigured

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

def reproduce_issue():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'
    try:
        django.setup()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
