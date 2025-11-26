from sympy import Range, Symbol, oo

def print_stacktrace(e: Exception):
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

def test_is_finite_set():
    r = Range(5)
    assert r.is_finite_set is not None, "is_finite_set property not implemented for Range"
    print("Test passed: is_finite_set property implemented for Range")

def test_sup_inf_with_symbolic_integer():
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        s.sup
    except ValueError as e:
        print_stacktrace(e)
        assert False, "sup does not work with symbolic integer"
    else:
        print("Test passed: sup works with symbolic integer")

test_is_finite_set()
test_sup_inf_with_symbolic_integer()
