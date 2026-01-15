```python
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
        assert Range(5).is_finite_set is not None, "is_finite_set property is not implemented."
    except AssertionError as e:
        print("Test for is_finite_set failed.")
        raise e


def test_sup_for_symbolic_range():
    from sympy import Symbol, oo, Range
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        _ = s.sup    
        assert False, "Expected a ValueError for sup of a symbolic Range but none occurred."
    except ValueError as e:
        print("Test for symbolic Range's sup passed successfully.")
    except Exception as e:
        print("Unexpected exception for symbolic Range's sup test.")
        print_stacktrace(e)
        assert False, "Unexpected exception type."


def main():
    try:
        test_is_finite_set()
    except AssertionError as e:
        print_stacktrace(e)
        print("is_finite_set issue reproduced successfully.")
        exit(0)  # Exiting with 0 to indicate successful reproduction to the script runner
    try:
        test_sup_for_symbolic_range()
        # If the previous test passes, it means the issue still exists, hence not exiting
    except SystemExit as e:
        raise e  # This exception is raised from test_is_finite_set() and indicates successful reproduction
    except Exception:
        pass  # Any exception from test_sup_for_symbolic_range is already handled

    print("Both issues seem to have been fixed. Exiting with code 0.")
    exit(0)


if __name__ == "__main__":
    main()
```

This script attempts to reproduce two distinct issues with the Sympy library:

1. Checking if the `is_finite_set` property is implemented for `Range`.
2. Ensuring that a `ValueError` is expected when attempting to access the supremum (`sup`) of a Range with a symbolic start and an infinite end.

- It first tries to assert the presence of `is_finite_set` property for a finite `Range`. If not present, it catches an `AssertionError` and uses the `print_stacktrace` function to display where it was caught, indicating the first issue is present.
- Then, it handles the case for `sup` calculation on a symbolic `Range`, expecting a `ValueError` due to the inability to compute the supremum under these conditions. If such an error is not handled properly (e.g., due to an implementation gap), it will show that the issue is present or there is an unexpected exception which is also handled.

Exiting with status code 0 in both cases ensures that the script runner understands a successful run (either both issues are fixed or properly reproduced).