import sympy as sp
from sympy.abc import x

def test_codegen():
    code = sp.fcode(sp.sign(x))
    assert "sign(1, x)" in code or "sign(1d0, x)" in code, f"Invalid Fortran syntax: {code}"

try:
    test_codegen()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
