import os
import sys
from django.core.management.commands.startproject import Command as StartProjectCommand

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
    os.umask(0o77)  # Set umask to 077
    os.makedirs('mysite', exist_ok=True)
    with open('mysite/settings.py', 'w') as f:
        pass

    try:
        start_project_command = StartProjectCommand()
        start_project_command.handle('myproject')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
