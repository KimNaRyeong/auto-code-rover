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
    
    for i in range(21):
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 + i * 0.0001 * x)], (x, y))
        
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

This script will run a loop that tests the `linsolve` function for different values of the coefficient in the second equation. If any test fails, it raises an `AssertionError`, which is then caught and printed with a stack trace.