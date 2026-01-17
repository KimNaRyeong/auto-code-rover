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
    from sympy import symbols, Subs

    # Define symbols
    x, y, a, z = symbols('x y a z')

    # Creating Subs objects as described in the issue
    obj_1 = Subs(x+y, (a,), (4,))
    obj_2 = Subs(x+y, (a,), (a,))
    obj_3 = obj_2.subs(a, z)

    # Attempt to assert the unexpected behavior
    try:
        assert obj_1 != obj_3, "Failure: obj_1 and obj_3 are unexpectedly equal."
        assert str(obj_3) == 'Subs(x + y, (a,), (z,))', "Failure: obj_3 does not match the expected output."

    except AssertionError as e:
        print_stacktrace(e)
        raise  # Reraise the exception to ensure the script exits due to the assertion

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError:
        # If an AssertionError is caught, it means the issue has been successfully reproduced.
        # The script will exit with a non-zero code to indicate failure (presence of the issue).
        exit(1)
    # If no issues are detected (i.e., no AssertionError is raised), print a success message and exit with 0.
    print("Issue reproduction attempt did not detect the problem. It might have been fixed.")
    exit(0)
