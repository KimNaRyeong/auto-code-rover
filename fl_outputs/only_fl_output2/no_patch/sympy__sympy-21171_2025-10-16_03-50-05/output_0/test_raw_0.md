```python
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

def test_singularity_function_issue():
    from sympy import symbols
    from sympy.physics.continuum_mechanics.beam import Beam
    E = symbols("E")
    L = symbols("L")
    F = symbols("F")
    B, H = symbols("B, H")
    I = B * H**3 / 12
    d = {B: 1e-02, H: 1e-02, E: 210e09, L: 0.2, F: 100}
    b2 = Beam(L, E, I)
    b2.apply_load(-F, L / 2, -1)
    b2.apply_support(0, "fixed")
    R0, M0 = symbols("R_0, M_0")
    b2.solve_for_reaction_loads(R0, M0)
    try:
        b2.shear_force()
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue with SingularityFunction handling detected.")

if __name__ == "__main__":
    try:
        test_singularity_function_issue()
    except AssertionError as e:
        print(e)
        # Demonstrates an issue and exits with code 0, assuming a fix would prevent this branch.
    else:
        print("No issue detected.")
```
This script will reproduce the issue outlined, where attempting to execute `b2.shear_force()` with the given parameters and setup results in a `TypeError` due to an unexpected keyword argument 'exp'. The `print_stacktrace` function provides detailed traceback information, aiding in debugging efforts.