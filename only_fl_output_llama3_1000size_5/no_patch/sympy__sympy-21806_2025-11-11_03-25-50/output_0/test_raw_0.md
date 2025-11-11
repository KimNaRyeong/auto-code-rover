Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_quaternion_evalf(self):
        try:
            q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
            q.evalf()
        except AttributeError as e:
            print_stacktrace(e)
            raise AssertionError("Quaternion class has no overridden evalf method")
        else:
            exit(0)

if __name__ == "__main__":
    Reproducer().run()
```

This script creates a test case that attempts to call the `evalf` method on a `Quaternion` object. If the `evalf` method is not found, it catches the `AttributeError`, prints the stack trace using the provided function, and raises an `AssertionError`.