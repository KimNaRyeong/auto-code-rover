# reproducer.py
import sympy as sy

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

def test_lambdify_with_curly_braces():
    curlyx = sy.symbols("{x}")
    v = sy.MatrixSymbol("v", 2, 1)
    curlyv = sy.MatrixSymbol("{v}", 2, 1)

    try:
        curlyScalarId = sy.lambdify(curlyx, curlyx)
        vectorId = sy.lambdify(v, v)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failure in handling scalar or vector with lambdify.") from e

    try:
        curlyVectorId = sy.lambdify(curlyv, curlyv)
        curlyVectorIdDummified = sy.lambdify(curlyv, curlyv, dummify=True)
        # If the code reaches this point without a SyntaxError,
        # it means the issue has been resolved.
        print("No issue detected with curly braces in MatrixSymbol name using lambdify.")
        exit(0)
    except SyntaxError as e:
        print_stacktrace(e)
        raise AssertionError("Detected issue with curly braces in MatrixSymbol name using lambdify.") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error during lambdify operations.") from e

if __name__ == "__main__":
    test_lambdify_with_curly_braces()
