# reproducer.py
import os
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def simulate_autoreloader_behavior(exception_instance):
    """
    Simulates the behavior of django.utils.autoreload.raise_last_exception
    which tries to re-raise exceptions by constructing a new exception
    of the same type with the original exception as its single argument.
    """
    exception_type = type(exception_instance)
    try:
        # Trying to construct a new exception of the same type with the original exception as its argument.
        raise exception_type(exception_instance)
    except TypeError as e:
        # If we catch a TypeError, this means the autoreloader's approach failed.
        return e
    except Exception as e:
        # If we successfully re-raise the exception, this path simulates the correct behavior.
        return None

def main():
    class MyException(Exception):
        def __init__(self, value: str, other_thing: str):
            super().__init__(value)
            self.ot = other_thing

    original_exception = MyException("foo", "bar")
    try:
        # This behavior simulates what Django's autoreloader does.
        e = simulate_autoreloader_behavior(original_exception)
        if e is None:
            print("The issue has been fixed.")
            sys.exit(0)
        else:
            raise AssertionError("The autoreloader's behavior of re-raising exceptions is incorrect.") from e
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
