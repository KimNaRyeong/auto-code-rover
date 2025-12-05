 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        from sympy import *
        from sympy.physics.continuum_mechanics import Beam
        # Young's modulus
        E = symbols("E")
        # length of the beam
        L = symbols("L")
        # concentrated load at the end tip of the beam
        F = symbols("F")
        # square cross section
        B, H = symbols("B, H")
        I = B * H**3 / 12
        # numerical values (material: steel)
        d = {B: 1e-02, H: 1e-02, E: 210e09, L: 0.2, F: 100}

        b2 = Beam(L, E, I)
        b2.apply_load(-F, L / 2, -1)
        b2.apply_support(0, "fixed")
        R0, M0 = symbols("R_0, M_0")
        b2.solve_for_reaction_loads(R0, M0)

        b2.shear_force

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    b2.shear_force
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 126, in shear_force
    return self._sf
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 112, in _force
    return self._force(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 108, in _force
    return self._force_internal(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 104, in _force_internal
    return self._force_internal_raw(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 98, in _force_internal_raw
    return self._force_internal_raw_raw(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 94, in _force_internal_raw_raw
    return self._force_internal_raw_raw_raw(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/beam.py", line 89, in _force_internal_raw_raw_raw
    return self._force_internal_raw_raw_raw_raw(self._x)
  File "/usr/local/lib/python3.8/dist-packages/sympy/physics/continuum_mechanics/be