Here is the reproducer script:

```python
import sympy
import traceback
import sys

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
    x, y = sympy.symbols('x, y')
    expected_result = (0, 0)
    
    for i in range(16):
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 + 0.0001 * i * x)], (x, y))
        
        if result != FiniteSet(expected_result):
            raise AssertionError("linsolve fails simple system of two equations")
    
    print("Issue not found")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
```

This script will run the `linsolve` function with different values of `y` and check if it returns the expected result. If any of these calls return a different result, an `AssertionError` is raised with the stack trace printed.