```python
# reproducer.py
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

def test_symmetric_sparse_matrix_generation():
    import sympy
    from sympy.matrices import randMatrix

    try:
        # Test case with percent=50, expecting symmetric matrix
        matrix_50_percent = randMatrix(3, symmetric=True, percent=50)
        for i in range(matrix_50_percent.rows):
            for j in range(matrix_50_percent.cols):
                if i != j and matrix_50_percent[i, j] != matrix_50_percent[j, i]:
                    raise AssertionError("Matrix is not symmetric at percent=50")

        # Test case with percent=0, expecting fully sparse (zero) matrix but symmetric
        matrix_0_percent = randMatrix(3, symmetric=True, percent=0)
        non_zero_elements = sum(1 for i in matrix_0_percent if i != 0)
        if non_zero_elements != 0:
            raise AssertionError("Matrix with percent=0 is not fully sparse")

        print("All tests passed! Issue cannot be reproduced.")

    except AssertionError as e:
        print_stacktrace(e)
        # Ensure the script exits with a non-zero exit code if AssertionError is caught
        sys.exit(-1)

if __name__ == "__main__":
    test_symmetric_sparse_matrix_generation()
```