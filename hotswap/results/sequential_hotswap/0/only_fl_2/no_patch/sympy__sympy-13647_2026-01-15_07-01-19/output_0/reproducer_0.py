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
