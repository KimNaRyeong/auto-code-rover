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

def main():
    from sympy import symbols, diophantine, Eq

    x, y, z = symbols('x y z')
    # Construct the equation as given in the issue.
    eq = Eq(x**2 + y**2 + z**4, 1 + 4 + 2**4)

    try:
        solutions = diophantine(eq)
        # Expecting solutions to be non-empty if the issue is addressed.
        # Assert fails if the solutions set is empty, indicating the issue is still present.
        assert solutions, "Diophantine equation incorrectly returned an empty solution set."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with a non-zero code to indicate the presence of the issue.
    except Exception as e:  # Catch any unexpected errors.
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
