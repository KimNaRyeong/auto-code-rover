Here is the reproducer script:

```python
import sympy as sp
from sympy import I, MatrixSymbol
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    M = MatrixSymbol('M', 2, 2)
    try:
        print(I * M)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError"

if __name__ == "__main__":
    main()
```

This script creates a `MatrixSymbol` and then tries to multiply it with the imaginary unit `I`. If the issue is present, an `AssertionError` will be raised when trying to run this script.