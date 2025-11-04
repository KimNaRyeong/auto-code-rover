Here is the reproducer script:

```python
import sympy
from sympy.core.sympify import kernS
from sympy import symbols, Eq

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
        x = symbols('x')
        text = "(2*x)/(x-1)"
        expr = kernS(text)  
        # hit = kern in s
        # UnboundLocalError: local variable 'kern' referenced before assignment
        assert False, "Expected error"
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` in your terminal.