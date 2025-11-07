import sympy as sp

def julia_code(s):
    return str(sp.julia_code(s))

try:
    code = julia_code('x**2*y*A**3')
    if not code.startswith("'(x.") or code.endswith(")A^3'"):
        raise AssertionError("Expected error")
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error"
