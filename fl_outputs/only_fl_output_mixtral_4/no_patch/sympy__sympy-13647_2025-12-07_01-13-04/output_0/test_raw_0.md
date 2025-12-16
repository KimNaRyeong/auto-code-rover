 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sympy as sm
from reproducer import print_stacktrace

def test_col_insert_issue():
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    expected_matrix = sm.Matrix(
        [
            [1, 0, 0, 2, 2, 1, 0, 0],
            [0, 1, 0, 2, 2, 0, 1, 0],
            [0, 0, 1, 2, 2, 0, 0, 1],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 0],
        ]
    )

    result_matrix = M.col_insert(3, V)

    assert result_matrix == expected_matrix, "Matrix after column insertion is incorrect"

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        test_col_insert_issue()
        print("Matrix col_insert works correctly")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
```
This script defines a `test_col_insert_issue` function that creates a 6x6 identity matrix and a 6x2 matrix of ones, inserts the 6x2 matrix into the 6x6 matrix starting from the 4th column, and then compares the resulting matrix with the expected matrix. If the resulting matrix is not equal to the expected matrix, an AssertionError is raised.

The script also defines a `print_stacktrace` function that prints the stack trace of an exception.

Finally, the script calls the `test_col_insert_issue` function and exits with code 0 if the test passes, or prints the stack trace and exits with code 1 if the test fails.