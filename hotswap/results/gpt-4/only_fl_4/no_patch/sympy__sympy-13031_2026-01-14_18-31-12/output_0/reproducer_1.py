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

def test_matrix_behavior():
    import sympy as sy
    # Test case with 0-dimensional matrices
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)
    
    hstack_result_zero = sy.Matrix.hstack(M1, M2, M3, M4).shape

    # Test case with 1-dimensional matrices
    M5 = sy.Matrix.zeros(1, 0)
    M6 = sy.Matrix.zeros(1, 1)
    M7 = sy.Matrix.zeros(1, 2)
    M8 = sy.Matrix.zeros(1, 3)
    
    hstack_result_one = sy.Matrix.hstack(M5, M6, M7, M8).shape
   
    try:
        # Ensure that horizontal stacking results are as expected
        assert hstack_result_zero != (0, 6), "Issue NOT present for 0-dimensional matrices"
        assert hstack_result_one == (1, 6), "Issue present with 1-dimensional matrices"
        
        # If the script did not raise an assertion, the issue has been fixed
        print("Issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_matrix_behavior()
        exit(0)   # Exit with code 0 indicating no issue found / issue fixed
    except AssertionError:
        exit(1)   # Exit with code 1 indicating the issue is present
