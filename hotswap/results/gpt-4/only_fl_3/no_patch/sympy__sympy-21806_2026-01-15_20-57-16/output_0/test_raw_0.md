```python
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
    import sympy as sp
    try:
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        result = q.evalf()  # Attempt to call evalf
        # Here we expected result to be a numerical evaluation but instead it just simplifies the expression.
        # So, we check if the result is an instance of sp.Quaternion to confirm if evalf behaved unexpectedly.
        assert not isinstance(result, sp.Quaternion), "evalf() method does not work as expected on Quaternion class."

    except AssertionError as e:
        print_stacktrace(e)
        raise

    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(0)  # Exit with code 0 to indicate the issue is present as expected
    except Exception:
        exit(1)  # Exit with a non-zero code to indicate an unexpected failure.
```

This script attempts to produce a numerical evaluation of a `Quaternion` object using SymPy by calling the `evalf()` method. If the `evalf()` method doesn't work as expected (i.e., it doesn't perform a numerical evaluation and instead returns a `Quaternion` object), it raises an `AssertionError`. The `AssertionError` is caught, and a stack trace of the issue is printed, highlighting the exact line where the issue occurs. The script exits with code 0 when the issue is reproduced successfully (signifying that the issue is present as described), and it exits with a non-zero code if an unexpected error occurs, indicating something else went wrong during execution.