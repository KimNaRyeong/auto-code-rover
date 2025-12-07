import sympy as sm
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

def test_col_insert_issue():
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    expected_matrix = sm.Matrix(
        [
            [1, 0, 0, 2, 2, 0, 0, 0],
            [0, 1, 0, 2, 2, 0, 0, 0],
            [0, 0, 1, 2, 2, 0, 0, 0],
            [0, 0, 0, 2, 2, 1, 0, 0],
            [0, 0, 0, 2, 2, 0, 1, 0],
            [0, 0, 0, 2, 2, 0, 0, 1],
        ]
    )

    result_matrix = M.col_insert(3, V)

    assert result_matrix == expected_matrix, "Matrix after column insertion is incorrect"

if __name__ == "__main__":
    try:
        test_col_insert_issue()
        print("Matrix col_insert works correctly")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
