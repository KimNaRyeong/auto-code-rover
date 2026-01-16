from sympy import exp, Matrix, simplify, sqrtdenest, trigsimp, I, cos, sin
import sys

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

def test_simplification():
    mat = exp(Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))
    simplified_mat = simplify(mat)
    further_simplified_mat = sqrtdenest(simplified_mat)
    final_simplified_mat = trigsimp(further_simplified_mat)
    # Check if sin(1) is correctly recognized in the output matrix
    try:
        assert final_simplified_mat[1, 0] == -sin(1), "simplification fails to recognize sin(1)"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_simplification()
    print("Issue not present, exiting with code 0.")
    sys.exit(0)
