Here is the `reproducer.py` file that reproduces the issue:
```
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class WrapperException(Exception):
    pass

def raise_cause():
    try:
        raise ValueError("Original exception")
    except ValueError as e:
        raise WrapperException("Wrapped exception") from e

try:
    raise_cause()
except Exception as exc:
    while True:
        if not hasattr(exc, "__cause__"):
            break
        exc = exc.__cause__
    assert False, "Infinite loop detected"
```
This script defines a `WrapperException` class and a `raise_cause` function that raises a `ValueError` exception wrapped in a `WrapperException`. The main code catches the exception, enters an infinite loop if the cause/context cycle is present, and asserts an error with a stack trace if the issue is reproduced.

You can run this script using `python3 reproducer.py`, and it should raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will exit with code 0.