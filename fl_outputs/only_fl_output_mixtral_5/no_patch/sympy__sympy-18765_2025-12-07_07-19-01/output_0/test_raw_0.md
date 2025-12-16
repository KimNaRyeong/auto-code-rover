 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    x = sp.Symbol('x')
    assert sp.Add(x, x, evaluate=True) == 2*x, "Addition with evaluate=True not working as expected"

    A = sp.MatrixSymbol('A', 2,2)
    assert sp.MatAdd(A, A, evaluate=True) == 2*A, "Matrix addition with evaluate=True not working as expected"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace if the issue is present, and exit with code 0 if the issue is fixed.