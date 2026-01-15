# reproducer.py
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

def test_sympy_singularity_function_printing():
    from sympy import symbols, init_printing
    from sympy.physics.continuum_mechanics.beam import Beam

    init_printing()

    E, I, w, l = symbols('E, I, w, l')
    Ra, Ma = symbols('R_a, M_a')

    b = Beam(2 * l, E, I)

    b.apply_load(Ra, 0, -1)
    b.apply_load(-Ma, 0, -2)
    b.apply_load(-w * l, l, -1)
    b.apply_load(-w / l, l, 1)
    b.apply_load(-w * l**2 / 2, 2 * l, -2)

    expected_load = "R_a*SingularityFunction(x, 0, -1) - M_a*SingularityFunction(x, 0, -2) - w*l*SingularityFunction(x, l, -1) - w/l*SingularityFunction(x, l, 1) - w*l**2/2*SingularityFunction(x, 2*l, -2)"

    try:
        assert str(b.load) == expected_load, "Singularity function powers do not print correctly."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sympy_singularity_function_printing()
    except AssertionError:
        # Ensure the script exits with a non-zero exit code when the assertion fails
        import sys
        sys.exit(1)
    else:
        # Exit with code 0 when the issue is fixed and the assertion passes
        sys.exit(0)
