import sympy
from sympy.matrices import randMatrix

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

def test_rand_matrix():
    for percent in (1, 50, 99, 0):
        matrix = randMatrix(3, symmetric=True, percent=percent)
        num_non_zero_elements = sum(1 for e in matrix.values() if e != 0)
        expected_non_zero_elements = int(percent / 100 * 6)
        assert num_non_zero_elements == expected_non_zero_elements, \
            f"Expected {expected_non_zero_elements} non-zero elements, but got {num_non_zero_elements}"

if __name__ == "__main__":
    try:
        test_rand_matrix()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
