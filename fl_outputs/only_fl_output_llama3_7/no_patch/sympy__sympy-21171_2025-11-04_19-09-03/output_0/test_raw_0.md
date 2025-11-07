Here is the reproducer script:

```python
import sympy as sp
from sympy.physics.continuum_mechanics import Beam
from sympy import symbols, Eq, solve

def main():
    try:
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

        b2.shear_force()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script should reproduce the issue when run with `python3 reproducer.py`.