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

def reproduce_issue():
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

    # Assume an expected incorrect string format for the load
    expected_incorrect_format = 'SingularityFunction(x, 0, -1)'
    actual_format = str(b.load)

    if expected_incorrect_format not in actual_format:
        print("The issue seems to be fixed!")
        sys.exit(0)

    raise AssertionError("Singularity function powers are not printed correctly.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
