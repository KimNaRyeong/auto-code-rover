Here is the reproducer script:

```python
import sympy
import unittest
from unittest.mock import patch

class C:
    def __repr__(self):
        return 'x.y'

class TestReproducer(unittest.TestCase):

    @patch('sympy.core.sympify')
    def test_reproducer(self, mock_sympify):
        with self.assertRaises(AssertionError) as e:
            sympy.Symbol('x') == C()
        print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script will run the reproducer and if the issue is present, it will raise an `AssertionError` and print a stack trace. If the issue is fixed, it will exit with code 0.