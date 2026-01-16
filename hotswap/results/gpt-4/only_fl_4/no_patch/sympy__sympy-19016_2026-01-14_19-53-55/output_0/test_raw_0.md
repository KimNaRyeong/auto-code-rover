Below is a standalone Python script that you can use to reproduce the issues described. The script checks for the implementation of `is_finite_set` in the `Range` class and also the behavior of `sup` and `inf` when one of the elements is a symbolic integer.

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

def test_is_finite_set_implemented():
    from sympy import Range
    assert hasattr(Range(5), 'is_finite_set'), "is_finite_set property is not implemented for Range."

def test_sup_inf_with_symbolic_integer():
    from sympy import Range, Symbol, oo
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        _ = s.sup
        _ = s.inf
        # (Place for future checks if needed)
    except ValueError as e:
        print_stacktrace(e)
        assert False, "sup/inf calculation with symbolic integer and Range failed."

def main():
    try:
        test_is_finite_set_implemented()
        test_sup_inf_with_symbolic_integer()
        print("All tests passed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script first checks if the `is_finite_set` property is implemented for the `Range` class by creating an instance of `Range` and asserting the existence of the `is_finite_set` attribute. It then proceeds to create a `Range` with a symbolic integer and tests if it can calculate the supremum (`sup`) and infimum (`inf`). If one of these assertions fails or any exception is caught during these tests, the script prints a detailed stack trace using the provided `print_stacktrace` function. The execution will proceed normally, indicating the issue has been fixed when these tests pass without asserting or raising an exception.