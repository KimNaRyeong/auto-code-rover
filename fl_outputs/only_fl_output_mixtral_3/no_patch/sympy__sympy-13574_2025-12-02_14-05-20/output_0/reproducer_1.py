import sys
import traceback
from sympy.matrices import randMatrix

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_rand_matrix():
    n = 3
    for percent in [1, 50, 99, 0]:
        matrix = randMatrix(n, symmetric=True, percent=percent)
        # Check if the matrix is symmetric
        for i in range(n):
            for j in range(i+1, n):
                assert matrix[i,j] == matrix[j,i], f"Matrix is not symmetric: {matrix}"
        # Check if the percentage of non-zero elements is approximately equal to the given percentage
        num_non_zero = sum(sum(1 for x in row if x != 0) for row in matrix)
        assert 0.95 * percent <= num_non_zero / n**2 <= 1.05 * percent, f"Unexpected number of non-zero elements: {num_non_zero}"

if __name__ == "__main__":
    try:
        test_rand_matrix()
        print("All tests passed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
