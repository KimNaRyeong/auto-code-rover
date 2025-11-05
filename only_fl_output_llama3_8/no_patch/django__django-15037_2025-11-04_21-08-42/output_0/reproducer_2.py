import os
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.core.management import call_command

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

def inspectdb_reproducer():
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        from django.core.management import call_command
        call_command('inspectdb')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    inspectdb_reproducer()
