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

def run_test():
    import pytest

    def test_approx():
        assert [1, 2] == pytest.approx([1.001, 2.002])
    
    try:
        test_approx()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)   # Ensure we exit with code 0 only when successful.
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)   # Handle unexpected errors.

    # If the assertion passes or pytest behaves as expected without numpy error, exit with 0.
    print("Test executed without the `ModuleNotFoundError: No module named 'numpy'.` issue.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
