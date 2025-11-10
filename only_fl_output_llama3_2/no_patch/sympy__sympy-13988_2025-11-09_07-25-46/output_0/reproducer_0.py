import sympy as sm
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestIntegralAsSum(unittest.TestCase):

    def test_integral_as_sum(self):
        t, t0, tf = sm.symbols('t, t0, tf')
        x = sm.Function('x')(t)
        y = sm.Function('y')(t)
        J = sm.Integral((x - y)**2, (t, t0, tf))
        f = StringIO()
        with redirect_stdout(f):
            print(J.as_sum(20, 'trapezoid'))
        output = f.getvalue().strip()
        expected_output = "Sum"
        self.assertNotEqual(output, expected_output)

    def test_integral_as_sum_doit(self):
        t, t0, tf = sm.symbols('t, t0, tf')
        x = sm.Function('x')(t)
        y = sm.Function('y')(t)
        J = sm.Integral((x - y)**2, (t, t0, tf))
        f = StringIO()
        with redirect_stdout(f):
            print(J.doit().as_sum(20, 'trapezoid'))
        output = f.getvalue().strip()
        expected_output = "Sum"
        self.assertEqual(output, expected_output)

    def test_integral_as_sum_doit_fails(self):
        t, t0, tf = sm.symbols('t, t0, tf')
        x = sm.Function('x')(t)
        y = sm.Function('y')(t)
        J = sm.Integral((x - y)**2, (t, t0, tf))
        try:
            print(J.doit().as_sum(20, 'trapezoid'))
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected Sum but got evaluated expression")

if __name__ == '__main__':
    unittest.main()
