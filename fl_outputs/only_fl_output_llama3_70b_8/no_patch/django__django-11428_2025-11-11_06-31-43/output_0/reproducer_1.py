import os
import sys
import traceback
from django.utils.autoreload import raise_last_exception

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

def raise_my_exception():
    try:
        raise MyException("foo", "bar")
    except Exception as e:
        raise_last_exception(*sys.exc_info())

try:
    raise_my_exception()
except TypeError as e:
    print_stacktrace(e)
    assert "missing 1 required positional argument" in str(e), "Issue not present"
    sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
