# reproducer.py

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
    import pytest

    def test_foo_dict():
        a = {'foo': 42.0}
        b = {'foo': 0.0}
        assert a == pytest.approx(b) # This should raise ZeroDivisionError in pytest/python_api.py

    def test_foo_list():
        a = [42.0]
        b = [0.0]
        assert a == pytest.approx(b) # This should pass

    try:
        test_foo_dict()
    except AssertionError as e:
        print("AssertionError as expected for 'test_foo_dict'")
    except Exception as e:
        print("Expected AssertionError for 'test_foo_dict', but got another exception:")
        print_stacktrace(e)
        sys.exit(1)  # Exit non-zero for unexpected exception types

    try:
        test_foo_list()
        print("test_foo_list passed as expected.")
    except Exception as e:
        print("Expected no exceptions for 'test_foo_list', but got:")
        print_stacktrace(e)
        sys.exit(1)  # Exit non-zero for any exception

if __name__ == "__main__":
    main()
    print("If no exception was raised for 'test_foo_dict', then the issue has likely been fixed.")
