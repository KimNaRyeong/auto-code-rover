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
    response_body_start = b'<!DOCTYPE html>'
    if response_body_start in output:
        raise AssertionError("Response body is not stripped for HEAD request")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

```
This script sets up a Django project, starts the development server, and then sends a HEAD request to the server using `curl`. It checks if the response body is stripped (i.e., not present) and raises an `AssertionError` if it's not. If the issue is fixed, the script will exit with code 0.

To use this script, create a new file named `reproducer.py` in the root directory of your project, copy-paste the above code into it, and then run it using `python3 reproducer.py`.