import os
import sys
from django.core.management import execute_from_command_line
from django.apps import apps

def main():
    # Set up the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    try:
        # Run makemigrations
        execute_from_command_line(['manage.py', 'makemigrations'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

    try:
        # Run migrate
        execute_from_command_line(['manage.py', 'migrate'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

    print("Issue fixed")

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

if __name__ == "__main__":
    main()
