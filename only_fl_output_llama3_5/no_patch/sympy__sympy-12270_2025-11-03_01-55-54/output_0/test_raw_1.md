Here is the standalone Python file `reproducer.py` to reproduce the issue:

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

def reproduce_bug():
    x, y = sp.symbols('x y')
    expr1 = -2*sp.sympify('x') - 4*sp.sympify('y') - 8
    try:
        result = expr1.extract_multiplicatively(-2)
        if not isinstance(result, (sp.Add, sp.Mul)):
            raise AssertionError("Expected a Mul or Add expression")
    except Exception as e:
        print_stacktrace(e)

reproduce_bug()
```

To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, it will raise an `AssertionError`, and you can see the stack trace with line numbers by running the script.