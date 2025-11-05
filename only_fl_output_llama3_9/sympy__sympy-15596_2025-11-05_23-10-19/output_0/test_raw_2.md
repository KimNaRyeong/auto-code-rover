Here is the reproducer script:

```python
import sympy as sp
from io import StringIO

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=StringIO())
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=StringIO())
        print(f"    {line_number}: {code_context}", file=StringIO())
    print(f"{e.__class__.__name__}: {e}", file=StringIO())

try:
    from sympy import Rational, symbols
    x = symbols('x')
    f = Rational((x-2)/(x**2+1), x)
    degree(f, x)
except Exception as e:
    print_stacktrace(e)
    raise

sys.exit(0)
```

This script attempts to compute the degree of a rational function using SymPy. If an exception is raised, it prints the stack trace and raises the same exception again.