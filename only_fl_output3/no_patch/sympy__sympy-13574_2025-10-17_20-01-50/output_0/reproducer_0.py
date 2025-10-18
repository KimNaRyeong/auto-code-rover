import sys
import sympy
from sympy.matrices import randMatrix

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_randMatrix_symmetric():
    try:
        # Test for 100 percent (should be symmetric and fully populated)
        matrix_100_percent = randMatrix(3, symmetric=True, percent=100)
        for i in range(matrix_100_percent.rows):
            for j in range(i, matrix_100_percent.cols):
                assert matrix_100_percent[i, j] == matrix_100_percent[j, i], "Matrix is not symmetric at 100 percent."

        # Test for 0 percent (should be symmetric and empty or have diagonal elements)
        matrix_0_percent = randMatrix(3, symmetric=True, percent=0)
        off_diagonal_elements = sum(matrix_0_percent[i, j] for i in range(matrix_0_percent.rows) for j in range(matrix_0_percent.cols) if i != j)
        assert off_diagonal_elements == 0, "Matrix has off-diagonal elements at 0 percent."

        # Test for percent values between 1 and 99 (should be symmetric)
        for percent in [1, 50, 99]:
            matrix_variable_percent = randMatrix(3, symmetric=True, percent=percent)
            for i in range(matrix_variable_percent.rows):
                for j in range(i, matrix_variable_percent.cols):
                    assert matrix_variable_percent[i, j] == matrix_variable_percent[j, i], f"Matrix is not symmetric at {percent} percent."

        print("All tests passed, no issue found.")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_randMatrix_symmetric()
    sys.exit(0)
