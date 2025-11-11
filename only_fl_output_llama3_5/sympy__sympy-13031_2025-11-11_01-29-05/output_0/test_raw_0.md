Here is the reproducer script:

```python
import sympy as sy
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestMatrixHStackVStack(unittest.TestCase):

    def test_matrix_hstack_vstack(self):
        try:
            M1 = sy.Matrix.zeros(0, 0)
            M2 = sy.Matrix.zeros(0, 1)
            M3 = sy.Matrix.zeros(0, 2)
            M4 = sy.Matrix.zeros(0, 3)
            result = sy.Matrix.hstack(M1, M2, M3, M4).shape
            self.assertEqual(result, (0, 6), "Expected (0, 6) but got {0}".format(result))
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

    def test_matrix_hstack_vstack_2(self):
        try:
            M1 = sy.Matrix.zeros(1, 0)
            M2 = sy.Matrix.zeros(1, 1)
            M3 = sy.Matrix.zeros(1, 2)
            M4 = sy.Matrix.zeros(1, 3)
            result = sy.Matrix.hstack(M1, M2, M3, M4).shape
            self.assertEqual(result, (1, 6), "Expected (1, 6) but got {0}".format(result))
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == '__main__':
    unittest.main()
```

This script defines a test case for the issue. It creates matrices with different shapes and checks if the expected shape is returned by `sy.Matrix.hstack` or `sy.Matrix.vstack`. If an assertion error occurs, it prints the stack trace and exits with code 1.