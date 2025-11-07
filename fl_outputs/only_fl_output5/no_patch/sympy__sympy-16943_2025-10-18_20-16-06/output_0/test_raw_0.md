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

def test_issue_12310():
    from sympy import Symbol, fps
    x = Symbol('x')
    p = fps(x ** 2)

    # Check if `p` is an instance of a formal power series
    assert hasattr(p, '__getitem__'), f"Expected a formal power series object, got {type(p)} instead."

    try:
        # Trying to access the first element to raise TypeError of `p` is not a formal power series.
        _ = p[0]
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("The issue #12310 is present.") from None

if __name__ == "__main__":
    try:
        test_issue_12310()
        print("No issue detected. The script executed successfully without raising an AssertionError.")
    except AssertionError:
        exit(1)  # Exit with a non-zero exit code to indicate an error
```

This script is designed to reproduce the issue as described. When executed, it attempts to use the `fps` function from SymPy to obtain a formal power series of `x**2`. It verifies whether the returned object supports indexing by trying to access its first element. If this operation does not raise a `TypeError`, it means the object supports indexing like a formal power series, and hence the script won't raise an `AssertionError`. Conversely, if accessing the first element causes a `TypeError`, indicating that the object does not behave as expected for a formal power series, the script will print the stack trace of the exception and terminate with exit code 1, signaling the presence of the issue (#12310).