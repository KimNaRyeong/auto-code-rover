Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sm

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

try:
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    M.col_insert(3, V)
    
    # Check if the identity matrix is shifted correctly
    expected_matrix = sm.Matrix([
        [1, 0, 0, 2, 2, 0],
        [0, 1, 0, 2, 2, 0],
        [0, 0, 1, 2, 2, 0],
        [0, 0, 0, 2, 2, 1],
        [0, 0, 0, 2, 2, 0],
        [0, 0, 0, 2, 2, 0]
    ])
    
    assert M.equals(expected_matrix), "Matrix.col_insert() does not work correctly"
    
    print("Issue is fixed!")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.