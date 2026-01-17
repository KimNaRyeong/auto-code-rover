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
    result = M.col_insert(3, V)
    expected_result = sm.Matrix([
        [1, 0, 0, 2, 2, 0, 0, 0],
        [0, 1, 0, 2, 2, 0, 0, 0],
        [0, 0, 1, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 1, 0, 0],
        [0, 0, 0, 2, 2, 0, 1, 0],
        [0, 0, 0, 2, 2, 0, 0, 1]
    ])
    try:
        assert result == expected_result, "Matrix.col_insert() does not work correctly."
    except AssertionError as e:
        print_stacktrace(e)
        raise

def main():
    try:
        test_matrix_col_insert()
    except AssertionError:
        exit(1)

if __name__ == "__main__":
    main()
    print("The issue has been fixed.")
