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

    M.col_insert(3, V)

    try:
        assert M.equals(expected_matrix)
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_col_insert_issue()
```
The `reproducer.py` file contains a single function `test_col_insert_issue()` that creates the given input matrices, constructs the expected matrix, performs the `col_insert()` operation, and checks if the resulting matrix is equal to the expected matrix using the `equals()` method.

The `print_stacktrace()` function is used to print the stack trace when the assertion fails.

To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised, and the stack trace will be printed. If the issue is fixed, the script will exit with code 0.