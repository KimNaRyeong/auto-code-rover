# reproducer.py
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

class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

def mimic_django_autoreload_raise(exception):
    """
    Mimics the behavior of django.utils.autoreload.raise_last_exception
    trying to reconstruct the exception instead of simply re-raising it.
    """
    try:
        # Mimic the problematic behavior
        exc_type = type(exception)
        new_exc = exc_type(exception)
        raise new_exc
    except TypeError as e:
        # If we encounter the TypeError, it indicates the issue is present.
        print("Issue detected: TypeError encountered during exception re-raise.")
        raise AssertionError("Autoreload exception re-raising issue present.") from e
    except MyException as re_raised_exception:
        # If the original exception is re-raised without issue, the issue is fixed.
        print("Original exception: ", re_raised_exception)
        print("No issue detected: Original exception re-raised successfully.")
        sys.exit(0)

def simulate_app_ready():
    """
    Simulates the Django AppConfig.ready() method where the original exception occurs.
    """
    raise MyException("foo", "bar")

try:
    simulate_app_ready()
except MyException as e:
    # Attempt to mimic the Django autoreload mechanism that captures and re-raises exceptions.
    try:
        mimic_django_autoreload_raise(e)
    except Exception as raised_exception:
        print_stacktrace(raised_exception)
        sys.exit(1)
