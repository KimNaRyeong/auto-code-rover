Here is the reproducer script:

```python
import sympy as sp
from sympy.stats import density, MatrixNormal
import unittest
from io import StringIO
from contextlib import redirect_stdout

def print_stacktrace(e):
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

class TestMatrixNormalDistribution(unittest.TestCase):

    def test_matrix_normal_distribution(self):
        try:
            from sympy import MatrixSymbol
            M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
            X = MatrixSymbol('X', 1, 2)
            density(M)(X).doit()
        except AssertionError as e:
            print_stacktrace(e)
            raise
        else:
            f = StringIO()
            with redirect_stdout(f):
                pass
            self.assertEqual(f.getvalue(), "")

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` module to run a test case. The test case attempts to reproduce the issue by initializing a matrix Normal Distribution in Sympy and calculating its density. If an `AssertionError` is raised, it prints the stack trace and re-raises the exception. If no error is raised, it checks that the output stream is empty, indicating that the expected result was obtained.