# reproducer.py
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

def test_matrix_col_insert():
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    M_updated = M.col_insert(3, V)
    
    # Expected matrix after correct column insertion
    expected_matrix = sm.Matrix([
        [1, 0, 0, 2, 2, 0, 0, 0],
        [0, 1, 0, 2, 2, 0, 0, 0],
        [0, 0, 1, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 1, 0, 0],
        [0, 0, 0, 2, 2, 0, 1, 0],
        [0, 0, 0, 2, 2, 0, 0, 1],
    ])

    try:
        assert M_updated == expected_matrix, "Matrix.col_insert() result is incorrect."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_matrix_col_insert()
    except AssertionError:
        exit(1)  # Exit with error code when assertion fails indicating the issue exists
    print("Issue not detected.")  # Only reaches here if the issue is fixed or not present
    exit(0)  # Exit with success code if no issue is detected
