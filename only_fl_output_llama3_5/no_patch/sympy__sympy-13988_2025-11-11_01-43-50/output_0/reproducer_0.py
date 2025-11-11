import sympy as sm
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestIntegralAsSum(unittest.TestCase):

    def test_integral_as_sum(self):
        with redirect_stdout(StringIO()):
            t, t0, tf = sm.symbols('t, t0, tf')
            x = sm.Function('x')(t)
            y = sm.Function('y')(t)
            J = sm.Integral((x - y)**2, (t, t0, tf))
            result = J.as_sum(20, 'trapezoid')

        expected_output = "Integral(as_sum) should output a Sum() object\n" + \
                          "Currently, Integral.as_sum() outputs an evaluated summation instead of an unevaluated expression:\n"

        self.assertEqual(result, None)
        self.assertEqual(StringIO().getvalue(), expected_output)

    def test_integral_as_sum_evaluates(self):
        with redirect_stdout(StringIO()):
            t, t0, tf = sm.symbols('t, t0, tf')
            x = sm.Function('x')(t)
            y = sm.Function('y')(t)
            J = sm.Integral((x - y)**2, (t, t0, tf))
            result = J.doit()

        expected_output = "-t0/20 + tf/20)*((x(t0/20 + 19*tf/20) - y(t0/20 + 19*tf/20))**2 + (x(t0/10 + 9*tf/10) - y(t0/10 + 9*tf/10))**2 + ..."

        self.assertEqual(result, None)
        self.assertEqual(StringIO().getvalue(), expected_output)

    def test_integral_as_sum_fails(self):
        with redirect_stdout(StringIO()):
            t, t0, tf = sm.symbols('t, t0, tf')
            x = sm.Function('x')(t)
            y = sm.Function('y')(t)
            J = sm.Integral((x - y)**2, (t, t0, tf))
            result = J.as_sum(20, 'trapezoid')

        expected_output = "Integral(as_sum) should output a Sum() object\n" + \
                          "Currently, Integral.as_sum() outputs an evaluated summation instead of an unevaluated expression:\n"

        self.assertRaises(AssertionError, print_stacktrace)
        self.assertEqual(StringIO().getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
