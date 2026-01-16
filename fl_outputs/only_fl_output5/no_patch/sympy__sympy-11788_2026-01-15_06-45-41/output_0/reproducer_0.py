import sys
from sympy import symbols, init_printing, pretty
from sympy.physics.continuum_mechanics.beam import Beam

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


init_printing()

E, I, w, l = symbols('E, I, w, l')
Ra, Ma = symbols('R_a, M_a')

try:
    b = Beam(2 * l, E, I)

    b.apply_load(Ra, 0, -1)
    b.apply_load(-Ma, 0, -2)
    b.apply_load(-w * l, l, -1)
    b.apply_load(-w / l, l, 1)
    b.apply_load(-w * l**2 / 2, 2 * l, -2)

    # Generating the pretty-printed string representation of the load
    load_string = pretty(b.load)

    # Assuming a simplified condition to simulate the expected correct or incorrect output
    # This is a simplified check; in a real situation, you might need to inspect the actual rendering
    # in the qtconsole or compare against a more comprehensive expected result pattern
    expected_substring = "l**(-1)"
    incorrect_substring = "l-1"

    if incorrect_substring in load_string:
        raise AssertionError("Singularity function powers are not printing correctly.")
    elif expected_substring not in load_string:
        raise AssertionError("The powers are not printed as expected, output might have changed.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed.")
sys.exit(0)
