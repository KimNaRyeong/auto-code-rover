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

def verify_symmetry(matrix):
    """
    Verifies if a given matrix is symmetric.
    """
    return all(matrix[i, j] == matrix[j, i] for i in range(matrix.rows) for j in range(matrix.cols))

def main():
    import sympy
    from sympy.matrices import randMatrix

    # Target to run the tests with different percent values.
    percents = [1, 50, 99, 0, 100]

    try:
        for percent in percents:
            matrix = randMatrix(3, symmetric=True, percent=percent)
            assert verify_symmetry(matrix), f"Matrix not symmetric with percent={percent}"
            print(f"Symmetry verified successfully with percent={percent}")
        
        # If the code reaches this point without an AssertionError, we consider the test passed.
        print("All tests passed. No issue detected.")
        
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
