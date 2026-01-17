# reproducer.py
from django.db.models import Q
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

def test_q_object_with_non_picklable():
    try:
        q = Q() | Q(x__in={}.keys())
    except TypeError as e:
        if "cannot pickle" in str(e):
            print_stacktrace(e)
            raise AssertionError("Issue with non-picklable object in Q detected.") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.") from e

if __name__ == "__main__":
    test_q_object_with_non_picklable()
    print("Test completed without issues.")
