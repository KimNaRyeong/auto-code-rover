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
    try:
        M = sm.eye(6)  # 6x6 identity matrix
        V = 2 * sm.ones(6, 2)  # 6x2 matrix filled with twos
        result = M.col_insert(3, V)  # Insert V into M at column index 3

        # Verify that the identity matrix portion is preserved correctly post-insertion
        for i in range(6):
            for j in range(8):  # The result matrix is now 6x8
                if i == j and i < 3:  # Before the insertion point
                    assert result[i, j] == 1
                elif i >= 3 and j >= 5 and (j - i) == 2:  # Proper position after the insertion
                    assert result[i, j] == 1
                elif (i < 3 and (j == 3 or j == 4)) or (i >= 3 and (j == 3 or j == 4)):
                    assert result[i, j] == 2  # Elements of V
                # Other cells should be 0
                else:
                    assert result[i, j] == 0

        print("Test passed. The issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with non-zero code to indicate failure

if __name__ == "__main__":
    test_matrix_col_insert()
