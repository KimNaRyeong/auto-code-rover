Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, Xor
from sympy.logic.boolalg import _finger
import pprint
import sys
import traceback

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
        A1, A2, A3 = symbols('A1:A3')
        f1 = Xor(A1, A2, A3)
        f2 = ~(Xor(A1, A2, A3))
        if sp.bool_map(f1, f2) != ((A1 & A2 & A3) | (A1 & ~A2 & ~A3) | (A2 & ~A1 & ~A3) | (A3 & ~A1 & ~A2), {A1: A1, A3: A3, A2: A2}):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def reproduce_fingerprint_issue():
    try:
        A1, A2, A3 = symbols('A1:A3')
        a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
        b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
        if a == b:
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def main():
    try:
        reproduce_issue()
        reproduce_fingerprint_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will run the reproducer for both issues and print the stack trace if any of them fail.