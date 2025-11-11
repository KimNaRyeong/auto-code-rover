Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x, y, z
import unittest

class TestIssue(unittest.TestCase):

    def test_issue(self):
        z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
        w = sp.expand(z)
        v = sp.factor(w)
        self.assertEqual(str(v), "0.0001*x**2 + 0.0005*x*y + 0.0004*y**2")

    def test_issue2(self):
        q_1, q_2, q_3 = sp.symbols('q_1 q_2 q_3')
        q = [q_1,q_2,q_3]
        Mq = sp.Matrix([[((1*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.sin(q_1)**2 + (1*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.cos(q_1)**2 + 0.25*sp.sin(q_1)**2*sp.cos(q_2)**2 + 0.25*sp.cos(q_1)**2*sp.cos(q_2)**2, 0, 0], [0, (-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.sin(q_1)**2 + (-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.cos(q_1)**2 + (-1*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))**2 + 0.25*sp.sin(q_1)**2*sp.sin(q_2)**2 + 0.25*sp.sin(q_2)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2)**2, -0.5*(-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-1*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3)], [0, -0.5*(-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-1*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-1*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3), 0.25*sp.sin(q_1)**2*sp.sin(q_2 + q_3)**2 + 0.25*sp.sin(q_2 + q_3)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2 + q_3)**2]])
        Mqs = sp.simplify(Mq)
        self.assertEqual(str(Mqs), "Matrix([[2.5, 0, 0], [0, 2.5, 0.75], [0, 0.75, 0.25]])")

    def test_issue3(self):
        z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
        w = sp.expand(z)
        v = sp.factor(w)
        if str(v) != "0.0001*x**2 + 0.0005*x*y + 0.0004*y**2":
            raise AssertionError("Incorrect result")
        q_1, q_2, q_3 = sp.symbols('q_1 q_2 q_3')
        q = [q_1,q_2,q_3]
        Mq = sp.Matrix([[((1*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.sin(q_1)**2 + (1*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**