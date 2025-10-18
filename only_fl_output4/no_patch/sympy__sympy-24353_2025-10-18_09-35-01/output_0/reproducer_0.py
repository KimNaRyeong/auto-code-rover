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

def test_sympy_benchmark_error():
    try:
        # Attempt to import the problematic module
        from sympy.utilities import benchmarking
        # If this point is reached, the originally reported issue cannot be reproduced.
        print("Issue 1741 appears to be fixed. Exiting with code 0.")
        exit(0)
    except ImportError as e:
        print_stacktrace(e)
        # Verifies that the ImportError is exactly what is expected from the issue description
        assert str(e) == "No module named __.test.item", "Unexpected ImportError message."

if __name__ == "__main__":
    test_sympy_benchmark_error()
