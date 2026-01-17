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

def run_test():
    from sympy import symbols, sstr
    from sympy.physics.continuum_mechanics.beam import Beam
    E, I, w, l = symbols('E, I, w, l')
    Ra, Ma = symbols('R_a, M_a')

    b = Beam(2 * l, E, I)

    b.apply_load(Ra, 0, -1)
    b.apply_load(-Ma, 0, -2)
    b.apply_load(-w * l, l, -1)
    b.apply_load(-w / l, l, 1)
    b.apply_load(-w * l**2 / 2, 2 * l, -2)

    expected_output = "R_a*SingularityFunction(x, 0, -1) - M_a*SingularityFunction(x, 0, -2) - w*l*SingularityFunction(x, l, -1) - w/l*SingularityFunction(x, l, 1) - w*l**2/2*SingularityFunction(x, 2*l, -2)"
    actual_output = sstr(b.load)

    # Attempting a basic check to see if the output matches the expected string representation.
    # This approach won't capture visual rendering issues in qtconsole but can verify functional correctness to some degree.
    if not expected_output == actual_output:
        raise AssertionError("Singularity function powers do not print correctly or there is a discrepancy in the representation.")

if __name__ == "__main__":
    try:
        run_test()
        print("Test passed: Issue not detected or has been fixed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        # Capture any unexpected error that might not be directly related to the AssertionError check.
        print_stacktrace(e)
        sys.exit(1)
