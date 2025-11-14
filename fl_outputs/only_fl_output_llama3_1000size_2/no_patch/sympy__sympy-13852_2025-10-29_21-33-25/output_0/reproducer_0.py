import sympy as sp
from sympy.abc import z, pi

def reproducer():
    try:
        result = sp.polylog(2, sp.Rational(1, 2)).expand(func=True).evalf()
        expected_result = -sp.log(2)**2/2 + pi**2/12
        if not sp.simplify(result - expected_result).is_zero:
            raise AssertionError("Expected result does not match")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproducer()
