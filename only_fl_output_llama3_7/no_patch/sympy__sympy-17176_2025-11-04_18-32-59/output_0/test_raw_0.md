Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols
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
        A1, A2, A3 = symbols('A1,A2,A3')
        f1 = sp.Xor(A1, A2, A3)
        f2 = ~sp.Xor(A1, A2, A3)
        print(sp.bool_map(f1, f2))
        
        a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
        b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
        pprint.pprint(a)
        pprint.pprint(b)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the given code and if any exception occurs, it will catch that exception, print the stack trace using `print_stacktrace` function and then re-raise the exception.