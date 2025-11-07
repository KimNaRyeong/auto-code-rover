Here is the reproducer script:

```python
import sympy as sp
from sympy.stats import density, MatrixNormal
import unittest
import sys
import traceback

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

class TestMatrixNormalDistribution(unittest.TestCase):

    def test_matrix_normal_distribution(self):
        try:
            from sympy import MatrixSymbol
            M = sp.MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
            X = sp.MatrixSymbol('X', 1, 2)
            density(M)(X).doit()
        except Exception as e:
            print_stacktrace(e)
            self.fail()

if __name__ == '__main__':
    unittest.main(exit=False)
    if len(sys.argv) > 1 and sys.argv[1] == 'fix':
        exit(0)
    else:
        exit(1)

```

To run this script, save it to a file named `reproducer.py` in the root directory of your project. Then, you can execute the script with Python: `python3 reproducer.py`.