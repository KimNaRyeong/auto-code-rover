import sympy as sp
from sympy.physics.continuum_mechanics import Beam
from io import StringIO
from contextlib import redirect_stdout

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

def run_and_check():
    try:
        from sympy import symbols, init_printing
        E, I, w, l = symbols('E, I, w, l')
        Ra, Ma = symbols('R_a, M_a')

        init_printing()

        b = Beam(2 * l, E, I)

        f = StringIO()
        with redirect_stdout(f):
            b.apply_load(Ra, 0, -1)
            b.apply_load(-Ma, 0, -2)
            b.apply_load(-w * l, l, -1)
            b.apply_load(-w / l, l, 1)
            b.apply_load(-w * l**2 / 2, 2 * l, -2)
            print(b.load)

        output = f.getvalue()
        if not output.startswith("Singularity function powers:"):
            raise AssertionError("Singularity function powers do not print correctly in the qtconsole")
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue reproduced successfully. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    run_and_check()
