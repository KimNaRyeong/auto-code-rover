Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_degree_rational_function(self):
        try:
            f = (sp.syymbols('x') - 2) / ((sp.syymbols('x'))**2 + 1)
            degree(f, 'x')
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Expected SymPy to compute degrees of rational functions")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

    if any((res.failures or res.errors) for res in test_result):
        sys.exit(1)
    else:
        sys.exit(0)
```

This script will run the `test_degree_rational_function` method, which attempts to compute the degree of a rational function using SymPy. If an exception is raised during this computation, it will print the stack trace and raise an `AssertionError`.