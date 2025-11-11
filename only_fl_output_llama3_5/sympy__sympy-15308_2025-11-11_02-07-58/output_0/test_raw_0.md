Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp

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

def reproduce_issue():
    try:
        n = 2
        A = sp.MatrixSymbol("A", n, n)
        latex_str = str(sp.latex(A**2))
        assert "A^2" in latex_str, f"Expected 'A^2' but got {latex_str}"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, simply execute `python3 reproducer.py` in your terminal. If the issue is present, it will print a stack trace and raise an `AssertionError`. If the issue is fixed, it will exit with code 0.