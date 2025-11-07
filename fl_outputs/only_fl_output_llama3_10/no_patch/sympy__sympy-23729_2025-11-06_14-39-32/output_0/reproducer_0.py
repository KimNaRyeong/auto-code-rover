import sympy as sp
from io import StringIO
from contextlib import redirect_stdout

def julia_code(expression):
    f = StringIO()
    with redirect_stdout(f):
        print(sp.julia_code(expression))
    return f.getvalue().strip()

expression = "x**2*y*A**3"
result = julia_code(expression)

if result == "(x.^2.*y)*A^3":
    raise AssertionError("Expected the output to have extra spaces")

print_stacktrace(AssertionError)
exit(1)  # Exit with code 1 when the issue is present
