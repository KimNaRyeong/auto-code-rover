Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
import subprocess
import time
import unittest
from io import StringIO
import contextlib

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
    try:
        os.chdir('django-test')
        with contextlib.redirect_stdout(StringIO()):
            with contextlib.redirect_stderr(StringIO()):
                execute_from_command_line(['manage.py', 'runserver'])
        output = StringIO.getvalue()
        expected_output = "HTTP/1.0 200 OK\nDate: Fri, 07 Apr 2017 14:56:39 GMT\nServer: WSGIServer/0.2 CPython/3.4.5\nContent-Type: text/html\nX-Frame-Options: SAMEORIGIN\n"
        if output != expected_output:
            raise AssertionError("Output does not match the expected output")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script will change into the `django-test` directory, run the Django development server using the `execute_from_command_line` function from the `django.core.management` module, and catch any exceptions that occur. It also checks if the output of the command matches the expected output. If it does not match or an exception is caught, it will print a stack trace using the provided `print_stacktrace` function and exit with code 1.