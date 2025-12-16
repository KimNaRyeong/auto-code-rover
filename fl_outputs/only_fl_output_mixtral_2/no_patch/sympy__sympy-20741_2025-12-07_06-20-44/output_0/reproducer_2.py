from sympy import MatrixSymbol, ZeroMatrix, simplify, expand, pprint, S
from sympy.matrices import eye
from sympy.abc import m, n
from sympy import init_printing
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

init_printing()

m = 3
n = 2

A = MatrixSymbol('A', m, n)
B = MatrixSymbol('B', m, n)
Z = ZeroMatrix(m, n)

expr = -(-A + B) - A + B
pprint(expr, use_unicode=True)
print("\nShould simplify to 0 when m =", m, "and n =", n)
print("But simplify() doesn't work as expected:\n")
print(expr.simplify())
print("\nHowever, expand() works:\n")
print(expand(expr))
print("\nAdding a zero matrix doesn't help:\n")
expr_with_zero = expr - Z
pprint(expr_with_zero, use_unicode=True)
print("\nShould simplify to 0 when m =", m, "and n =", n)
print("But simplify() still doesn't work as expected:\n")
print(expr_with_zero.simplify())
print("\nHowever, expand() still works:\n")
print(expand(expr_with_zero))

try:
    assert simplify(expr) == S(0)
except AssertionError:
    print_stacktrace(AssertionError("Simplification doesn't work as expected"))
    sys.exit(1)

sys.exit(0)
