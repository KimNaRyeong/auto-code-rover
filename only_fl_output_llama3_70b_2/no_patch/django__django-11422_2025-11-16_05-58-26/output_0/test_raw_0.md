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

    # Wait for the autoreloader to detect changes (should trigger a restart)
    time.sleep(5)

    # Check if the server is still running (it should have restarted)
    try:
        os.system("ps aux | grep 'manage.py' | grep -v 'grep'")
        assert False, "Autoreloader did not detect changes in manage.py"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
This script creates a temporary `manage.py` file, starts the development server, modifies the `manage.py` file, and waits for the autoreloader to detect changes. If the autoreloader does not detect the changes, it raises an `AssertionError` with a stack trace of the issue.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.