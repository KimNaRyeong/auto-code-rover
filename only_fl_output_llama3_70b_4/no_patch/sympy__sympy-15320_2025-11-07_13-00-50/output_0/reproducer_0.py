import sympy

def test_issue():
    x = sympy.symbols('x')
    t = sympy.symbols('t')

    # Test 1
    root_of_1 = sympy.RootOf(x**3 + x - 1, 0)
    assert root_of_1.poly.gen == x, "Generator is not x"
    
    # Test 2
    root_of_2 = sympy.RootOf((x**3+x-1).subs(x,t), 0)
    assert root_of_2.poly.gen == t, "Generator is not tan(x)"
    
    # Test 3
    root_of_3 = sympy.RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
    assert root_of_3.poly.gen == x, "Generator is not x"
    
    # Test 4
    root_of_4 = sympy.RootOf((x**3+2*x-1), 0)
    assert root_of_4.poly.gen != tan(x), "Generator should be x, but got tan(x)"

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

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
