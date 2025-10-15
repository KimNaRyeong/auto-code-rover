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

try:
    from sympy import symbols, diophantine
    from sympy.abc import x, y, z

    # Defining the equation
    eq = x**2 + y**2 + z**4 - (1 + 4 + 2**4)

    # Attempting to solve the diophantine equation
    solutions = diophantine(eq)

    # Checking if the solution set is empty, which should not be the case for a correct implementation
    assert solutions != set([]), "No solution found - potential issue with handling mixed even powers."

    # If the script reached this point without an assertion error, then it did not detect the expected issue.
except AssertionError as e:
    print("Issue detected as expected.")
    print_stacktrace(e)
    raise SystemExit(1)
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("No issue detected, which indicates potential resolution of the problem.")
    SystemExit(0)
