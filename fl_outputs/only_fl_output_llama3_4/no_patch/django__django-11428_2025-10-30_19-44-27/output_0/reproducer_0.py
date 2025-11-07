import os
import sys
from django.apps import AppConfig
from django.utils.autoreload import raise_last_exception
from django.core.management import execute_from_command_line

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

def reproduce_issue():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config'
    execute_from_command_line(['manage.py', 'runserver'])

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected the issue to be present"
else:
    print("Issue not present")
    sys.exit(0)

