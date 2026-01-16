Certainly! Below is a standalone Python file named `reproducer.py` that you can use to reproduce the issue mentioned. This script checks if the `col_insert` method of a SymPy Matrix behaves as expected. If the method does not work as intended (i.e., the issue is present), it raises an `AssertionError` and prints a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

```python
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

def test_col_insert():
    import sympy as sm

    # Create a 6x6 identity matrix
    M = sm.eye(6)

    # Create a 6x2 matrix with all elements equal to 2
    V = 2 * sm.ones(6, 2)

    # Insert V into M at column 3
    result = M.col_insert(3, V)

    expected = sm.Matrix([
        [1, 0, 0, 2, 2, 0, 0, 0],
        [0, 1, 0, 2, 2, 0, 0, 0],
        [0, 0, 1, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 1, 0, 0],
        [0, 0, 0, 2, 2, 0, 1, 0],
        [0, 0, 0, 2, 2, 0, 0, 1]
    ])

    # Check if the result matches the expected output
    assert result == expected, "Matrix.col_insert() did not work correctly."

if __name__ == "__main__":
    try:
        test_col_insert()
        print("No issues detected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

To use this script:

1. Save it as `reproducer.py` in the root directory of your project.
2. Run it with Python 3 by executing the command `python3 reproducer.py` in your terminal or command prompt.

The script tries to insert a matrix of twos into an identity matrix and checks if the operation results in the expected matrix layout. If the operation does not behave as expected (due to a bug or issue in the SymPy library), it will raise an `AssertionError`. If the issue has been resolved in the version of SymPy you're using, the script will print "No issues detected." and exit cleanly.