Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

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
    test.test_degree_rational_function()
```

This script defines a `Reproducer` class that inherits from `TestCase`. The `test_degree_rational_function` method attempts to call `degree(f, 'x')`, which should raise an exception if the issue is present. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.