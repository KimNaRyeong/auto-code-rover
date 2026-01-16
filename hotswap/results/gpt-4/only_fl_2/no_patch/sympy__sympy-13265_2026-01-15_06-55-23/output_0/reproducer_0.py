from sympy import Matrix, exp, simplify, I, trigsimp
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


def test_simplification_issue():
    # Performing matrix exponential operation
    mat_exponent = exp(Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))
    
    # Trying to simplify the exponential matrix
    simplified_mat = simplify(mat_exponent)

    # Applying further trigonometric simplification
    trig_simplified_mat = trigsimp(simplified_mat)

    # Checking if sin(1) is successfully simplified
    if I*exp(I) - I*exp(-I) not in trig_simplified_mat:
        print("Issue still present, trigonometric simplification failed to recognize sin(1).")
        raise AssertionError("Trigonometric simplification failed for sin(1).")
    else:
        print("Issue fixed, trigonometric simplification succeeded for sin(1).")


def main():
    try:
        test_simplification_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to indicate failure
    except Exception as e:
        print("An unexpected error occurred.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)  # Exit with success code to indicate issue is resolved


if __name__ == "__main__":
    main()
