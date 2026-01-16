Given your request, the Python script named `reproducer.py` below aims to explicitly reproduce the described issues. It will attempt to use the `is_finite_set` property from a `Range` object and handling of `sup` on a `Range` with symbolic bounds. The script will raise `AssertionError` when it encounters unsupported behavior (i.e., issues that are present) and will try to provide clear stack traces for debugging purposes. When issues are fixed, it is expected to exit with status code 0 without errors.

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

def test_is_finite_set():
    from sympy import Range
    try:
        # Attempt to access the is_finite_set property
        result = Range(5).is_finite_set
        if result is None:
            raise AssertionError("is_finite_set not properly implemented for Range")
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("is_finite_set property not found in class Range")

def test_sup_with_symbolic_range():
    from sympy import Symbol, oo, Range
    n = Symbol('n', integer=True)
    try:
        s = Range(n, oo, 1)
        sup = s.sup
        raise AssertionError("`sup` should raise a ValueError for symbolic ranges extending to infinity")
    except ValueError:
        # Expected behavior, pass silently
        pass
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected exception type caught")

def main():
    test_is_finite_set()
    test_sup_with_symbolic_range()
    print("All tests passed. The issues seem to be fixed.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"Test failed: {error}")
    else:
        exit(0)
```

**How to Use This Script:**

1. Place `reproducer.py` in the root directory of the Sympy project (or any desired Python environment where Sympy is installed).
2. Execute the script using Python 3: `python3 reproducer.py`.
   - If any issue is correctly reproduced, the script will raise an `AssertionError` and print a detailed stack trace for that specific problem.
   - If both the `is_finite_set` implementation and the handling of `sup` with symbolic ranges are working as expected (or the issues have been fixed), the script will print "All tests passed. The issues seem to be fixed." and exit with code 0.

This approach ensures a straightforward verification process for developers or contributors aiming to fix the issues, providing clear feedback on what's wrong and confirming when problems have been resolved.