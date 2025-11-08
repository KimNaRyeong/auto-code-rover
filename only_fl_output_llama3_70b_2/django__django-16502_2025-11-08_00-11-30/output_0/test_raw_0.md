Here is the `reproducer.py` script to reproduce the issue:
```
import os
import sys
from django.core.management import execute_from_command_line
from django.test.utils import get_runner

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test.settings'
    execute_from_command_line(['manage.py', 'runserver'])

    import subprocess
    output = subprocess.check_output(['curl', '-iX', 'HEAD', 'http://127.0.0.1:8000/'])
    response_lines = output.decode().splitlines()
    body_start = False
    for line in response_lines:
        if line.strip() == '':
            body_start = True
        elif body_start:
            assert False, "Response body should not be present"
            print_stacktrace(AssertionError("Response body should not be present"))
            sys.exit(1)

if __name__ == '__main__':
    main()
```
This script sets up a Django project and runs the development server. It then uses `curl` to send a HEAD request to the server and checks if the response contains a body. If it does, it raises an `AssertionError` with a stack trace.

To use this script, create a new file named `reproducer.py` in the root directory of your project, copy the above code into it, and run it using `python3 reproducer.py`.