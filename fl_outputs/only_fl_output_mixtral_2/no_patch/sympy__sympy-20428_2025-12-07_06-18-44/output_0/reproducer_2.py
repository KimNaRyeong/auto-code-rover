import sys
import traceback
from sympy import symbols, Poly, sqrt

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = symbols("x")
    f = Poly(
        -117968192370600 * 18 ** (1/3) / (217603955769048 * (24201 + 253 * sqrt(9165)) ** (1/3) + 2273005839412 * sqrt(9165) * (24201 + 253 * sqrt(9165)) ** (1/3)) + \
        15720318185 * 2 ** (2/3) * 3 ** (1/3) * (24201 + 253 * sqrt(9165)) ** (2/3) / (217603955769048 * (24201 + 253 * sqrt(9165)) ** (1/3) + 2273005839412 * sqrt(9165) * (24201 + 253 * sqrt(9165)) ** (1/3)) - \
        15720318185 * 12 ** (1/3) * (24201 + 253 * sqrt(9165)) ** (2/3) / (217603955769048 * (24201 + 253 * sqrt(9165)) ** (1/3) + 2273005839412 * sqrt(9165) * (24201 + 253 * sqrt(9165)) ** (1/3)) + \
        117968192370600 * 2 ** (1/3) * 3 ** (2/3) / (217603955769048 * (24201 + 253 * sqrt(9165)) ** (1/3) + 2273005839412 * sqrt(9165) * (24201 + 253 * sqrt(9165)) ** (1/3)),
        x
    )
    coeff, bad_poly = f.clear_denoms()
    assert bad_poly.is_zero == False
    assert bad_poly.as_expr() == 0
    print(bad_poly.terms_gcd())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
