import os
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

class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

def main():
    try:
        raise MyException("foo", "bar")
    except Exception as e:
        try:
            # Simulate django.utils.autoreload.raise_last_exception behavior
            raise type(e)(str(e))
        except TypeError as te:
            print_stacktrace(te)
            assert False, "Issue is present: Autoreloader crashes on re-raising exceptions with custom signature"
    else:
        print("Issue is fixed")

if __name__ == "__main__":
    main()
    sys.exit(0)
