Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy import Matrix, exp, I

def main():
    m = exp(Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]))
    simplified_m = sp.simplify(m)
    assert simplified_m[0, 1] == -sp.sin(1), "Simplification failed to recognize sin expressed as exponentials"
    print("Issue not present")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.