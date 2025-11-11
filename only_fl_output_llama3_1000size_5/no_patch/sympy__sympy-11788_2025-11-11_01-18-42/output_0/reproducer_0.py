import sympy as sp
from sympy.physics.continuum_mechanics import Beam
from io import StringIO
from contextlib import redirect_stdout
import unittest
from unittest.mock import patch, MagicMock

class TestSingularityFunctionPowers(unittest.TestCase):

    def test_singularity_function_powers(self):
        with self.assertRaises(AssertionError) as e:
            with redirect_stdout(StringIO()):
                from sympy.physics.continuum_mechanics import Beam
                E, I, w, l = sp.symbols('E, I, w, l')
                Ra, Ma = sp.symbols('R_a, M_a')

                b = Beam(2 * l, E, I)

                b.apply_load(Ra, 0, -1)
                b.apply_load(-Ma, 0, -2)
                b.apply_load(-w * l, l, -1)
                b.apply_load(-w / l, l, 1)
                b.apply_load(-w * l**2 / 2, 2 * l, -2)
                print(b.load)

        self.print_stacktrace(e)

    def print_stacktrace(self, e):
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

if __name__ == '__main__':
    unittest.main()
