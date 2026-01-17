# reproducer.py
import pytest

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

def test_foo_dict():
    a = {'foo': 42.0}
    b = {'foo': 0.0}
    try:
        assert a == pytest.approx(b)  # Potentially raises ZeroDivisionError
    except ZeroDivisionError as e:
        print("ZeroDivisionError encountered in test_foo_dict as expected.")
        print_stacktrace(e)
        exit(0)  # Exits with code 0 indicating the specific issue was reproduced
    except Exception as e:
        print("An unexpected exception occurred.")
        print_stacktrace(e)
        exit(1)  # Exits with code 1 indicating an unexpected issue
    print("test_foo_dict passed without encountering a ZeroDivisionError, which is unexpected.")
    exit(1)  # Exits with code 1 as the ZeroDivisionError was expected but did not occur

def test_foo_list():
    a = [42.0]
    b = [0.0]
    try:
        assert a == pytest.approx(b) # Should not raise ZeroDivisionError
    except AssertionError as e:
        print("AssertionError encountered in test_foo_list as expected, no ZeroDivisionError.")
        exit(0)  # Exits with code 0 as the behavior is as expected
    except Exception as e:
        print("An unexpected exception occurred in test_foo_list.")
        print_stacktrace(e)
        exit(1)  # Unexpected behaviour

if __name__ == "__main__":
    test_foo_dict()
    test_foo_list()
