import sympy as sp
from io import StringIO
from contextlib import redirect_stdout

def julia_code(s):
    f = StringIO()
    with redirect_stdout(f):
        print(sp.julia_code(s))
    return f.getvalue().strip()

def test_julia_code():
    code = julia_code('x**2*y*A**3')
    if '.*' in code:
        raise AssertionError("Invalid Julia code generated")
    else:
        print("Issue fixed")

try:
    test_julia_code()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present, all good!")
exit(0)
