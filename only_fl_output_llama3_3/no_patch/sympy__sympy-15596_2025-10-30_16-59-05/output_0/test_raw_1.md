Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_degree_rational_function(self):
        try:
            f = (sp.sympify('x-2')) / (sp.sympify('x**2+1'))
            degree(f, 'x')
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Expected SymPy to compute the degree of a rational function")

if __name__ == '__main__':
    test = Reproducer()
    try:
        test.test_degree_rational_function()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script defines a `Reproducer` class that inherits from `TestCase`. The `test_degree_rational_function` method attempts to call `degree(f, 'x')`, which should raise an exception if the issue is present. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.