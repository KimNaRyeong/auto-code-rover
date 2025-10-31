Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, tanh, csch, sech, csc, sec
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

def reproduce_issue():
    x, y = symbols('x y')
    try:
        result1 = sp.expand_trig(tanh(x + y))
        result2 = sp.expand_trig(csch(x + y))
        result3 = sp.expand_trig(sech(x + y))
        if not (result1 == (tanh(x) + tanh(y))/(tanh(x)*tanh(y) + 1) and \
               result2 == csch(x + y) and \
               result3 == sech(x + y):
            raise AssertionError("Expected csch and sech to expand as in csc and sec")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `expand_trig` function on `tanh(x+y)`, `csch(x+y)` and `sech(x+y)`, and check if the results are as expected. If not, it will raise an `AssertionError` with a stack trace.