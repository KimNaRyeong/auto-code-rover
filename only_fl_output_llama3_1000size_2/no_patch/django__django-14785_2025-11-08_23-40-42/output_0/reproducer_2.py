import os
import django
from django.db import models
from django.core.management import execute_from_command_line
from django.conf import settings

def main():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'issue_reproducer.settings')
    try:
        django.setup()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

    from issue_reproducer.models import MyModel

    try:
        # Create a model instance with NaN value
        obj = MyModel.objects.create(value=float('nan'))

        # Try to retrieve the object from database
        obj.refresh_from_db()
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

    if os.name == 'posix':
        execute_from_command_line(['python', 'manage.py', 'shell'])
    else:
        execute_from_command_line(['python', 'manage.py', 'shell'])

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

if __name__ == '__main__':
    main()

print_stacktrace
