Here is the reproducer script:

```python
import sympy as sy
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestMatrixHStackVStack(unittest.TestCase):

    def test_matrix_hstack_vstack(self):
        f = StringIO()
        with redirect_stdout(f):
            try:
                M1 = sy.Matrix.zeros(0, 0)
                M2 = sy.Matrix.zeros(0, 1)
                M3 = sy.Matrix.zeros(0, 2)
                M4 = sy.Matrix.zeros(0, 3)
                result = sy.Matrix.hstack(M1, M2, M3, M4).shape
                self.assertEqual(result, (0, 6), "Matrix hstack returns incorrect shape")
            except Exception as e:
                print_stacktrace(e)
                raise

        f.seek(0)
        output = f.getvalue()
        if not output.startswith("AssertionError"):
            with open('output.txt', 'w') as f:
                f.write(output)

    def print_stacktrace(self, e):
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

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` framework to run a test case. The test case creates matrices with different shapes and tries to stack them horizontally using `sy.Matrix.hstack`. If an assertion error occurs, it prints the stack trace and raises the exception again.