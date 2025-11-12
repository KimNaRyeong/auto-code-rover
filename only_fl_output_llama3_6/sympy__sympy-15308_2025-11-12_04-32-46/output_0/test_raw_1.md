Here is the reproducer script:

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
        if latex(trace(A**2)) != r'\mathrm{Trace}\left(\left[\begin{smallmatrix}A & 0 \\ 0 & A\end{smallmatrix}\right]^{2}\right)':
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, save it to a file named `reproducer.py` and then execute it with `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.