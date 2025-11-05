Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
    # Create a new Django project
    os.system("django-admin startproject django_test")
    os.chdir("django_test")

    # Start the development server
    execute_from_command_line(["manage.py", "runserver"])

    # Make an HTTP HEAD request to the server
    import subprocess
    output = subprocess.check_output(["curl", "-iX", "HEAD", "http://127.0.0.1:8000/"])

    # Check if the response body is empty
    assert b"<!DOCTYPE html>" not in output, "Response body is not empty"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```
This script creates a new Django project, starts the development server, makes an HTTP HEAD request to the server using `curl`, and checks if the response body is empty. If the response body is not empty, it raises an `AssertionError` with a stack trace of the issue.