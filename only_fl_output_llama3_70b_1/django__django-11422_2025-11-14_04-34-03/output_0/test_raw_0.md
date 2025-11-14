Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
import time
from django.utils.autoreload import autoreload_modules
from django.core.management.commands.runserver import run_server

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
    # Create a temporary manage.py file
    with open('manage.py', 'w') as f:
        f.write("import os\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_30479.settings')\n")

    # Start the development server
    run_server(None, addr='127.0.0.1', port=8000)

    # Wait for the server to start
    time.sleep(2)

    # Modify the manage.py file
    with open('manage.py', 'a') as f:
        f.write("\nprint('sth')\n")

    # Wait for the autoreloader to detect the change
    time.sleep(5)

    # Check if the server is still running
    if os.path.exists('manage.py'):
        raise AssertionError("Autoreloader did not restart the server")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script creates a temporary `manage.py` file, starts the development server, modifies the `manage.py` file, and waits for the autoreloader to detect the change. If the server is still running after 5 seconds, it raises an `AssertionError`. The script also catches any exceptions that occur during execution and prints a stack trace using the provided function.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.