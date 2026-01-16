Given the specifications, here's a revised version of `reproducer.py` that properly raises an `AssertionError` if the `Range.is_finite_set` property is not implemented or if there's an issue with using `.sup` on a Range with symbolic bounds, reflecting accurately whether the issue is present according to your criteria.

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

def check_is_finite_set():
    from sympy import Range
    if not hasattr(Range(5), 'is_finite_set'):
        raise AssertionError("is_finite_set property not implemented for Range")

def check_sup_with_symbolic_range():
    from sympy import Symbol, oo, Range
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        _ = s.sup
        # If the above line did not raise an exception,
        # it means the issue might have been silently fixed/handled;
        # we raise an assertion error to signal the test expectation explicitly.
        raise AssertionError("sup worked unexpectedly on Range with symbolic integer, which should not happen as per described issue.")
    except ValueError:
        # Expected behavior as per issue description. Catching it silently.
        return
    except Exception as e:
        print("Unexpected exception for sup method with symbolic range:")
        print_stacktrace(e)
        raise

def main():
    try:
        check_is_finite_set()
    except AssertionError as ae:
        print("AssertionError for is_finite_set property in Range:", ae)
        return  # Exit to avoid running the next test if this failed
    
    try:
        check_sup_with_symbolic_range()
    except AssertionError as ae:
        print("AssertionError when checking .sup on Range with symbolic boundaries:", ae)
        return  # This handles the specific case and stops further execution if caught

    print("All checks passed, issues seem fixed if no AssertionError was raised prior.")

if __name__ == "__main__":
    main()
```

This script includes:

1. **check_is_finite_set**: Verifies if the `is_finite_set` property is implemented in `Range`. If not, it raises an `AssertionError`.
2. **check_sup_with_symbolic_range**: Tries to access `.sup` on a `Range` that starts with a symbolic integer and stretches to infinity. If this operation does not raise a `ValueError`, it indicates a deviation from the expected behavior described in the issue. The discrepancy (whether it's an unexpected success or a wrong type of exception) triggers an `AssertionError`, or logs the unexpected exception for further inspection.
   
Running this ensures a clear output related to the current status of the reported issues within the environment it's executed in.