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

def reproduce_issue():
    curlyx = sy.symbols("{x}")
    v = sy.MatrixSymbol("v", 2, 1)
    curlyv = sy.MatrixSymbol("{v}", 2, 1)

    # Check if lambdify works with scalar and vector symbols without curly braces
    try:
        curlyScalarId = sy.lambdify(curlyx, curlyx)
        vectorId = sy.lambdify(v, v)
    except Exception as e:
        print("Exception occurred with lambdify using simple symbols:")
        print_stacktrace(e)
        raise AssertionError("Failed on symbols without curly braces.") from e
    
    # Check if lambdify fails with curly braces in MatrixSymbol name
    try:
        curlyVectorId = sy.lambdify(curlyv, curlyv)
    except SyntaxError as e:
        print("SyntaxError as expected with curly braces in MatrixSymbol name. Trying dummify=True...")
    except Exception as e:
        print("Unexpected exception occurred with curly braces in MatrixSymbol:")
        print_stacktrace(e)
        raise AssertionError("Failed in an unexpected manner.") from e
    else:
        raise AssertionError("Did not fail with curly braces in MatrixSymbol name as expected.")

    # Check if dummify=True solves the issue
    try:
        curlyVectorIdDummified = sy.lambdify(curlyv, curlyv, dummify=True)
    except Exception as e:
        print("Exception occurred with lambdify using curly braces in MatrixSymbol name even with dummify=True:")
        print_stacktrace(e)
        raise AssertionError("Failed with dummify=True on MatrixSymbol with curly braces.") from e
    else:
        # The script should not reach this point based on the described issue
        print("No error with lambdify using curly braces in MatrixSymbol name and dummify=True. Issue might have been fixed.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        raise
    else:
        exit(0)
