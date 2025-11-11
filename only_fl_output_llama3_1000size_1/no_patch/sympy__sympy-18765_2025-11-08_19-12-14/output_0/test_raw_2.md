Here is the reproducer script:

```python
import sympy as sp
from sympy import Add, MatAdd, Symbol, MatrixSymbol
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
    x = Symbol('x')
    assert Add(x, x).doit() == 2*x
    assert Add(x, x, evaluate=True) == 2*x
    
    A = MatrixSymbol('A', 2, 2)
    try:
        assert MatAdd(A, A).doit() == 2*A
        assert MatAdd(A, A, evaluate=True) != 2*A
        raise AssertionError("Expected MatAdd(A, A, evaluate=True) to be equal to 2*A")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will run the given code and check if the issue is present. If the issue is present, it will raise an `AssertionError` and print the stack trace of the error.