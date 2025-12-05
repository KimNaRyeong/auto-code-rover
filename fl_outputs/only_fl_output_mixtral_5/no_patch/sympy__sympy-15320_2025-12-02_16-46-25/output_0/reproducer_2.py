from sympy import RootOf, symbols, poly, tan
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

x = symbols('x')

# Reproduce the issue
root_of_1 = RootOf(x**3 + x - 1, 0)
print(root_of_1.poly.gen)  # Should print x, but prints x

root_of_2 = RootOf((x**3 + x - 1).subs(x, symbols('tan(x)')), 0)
print(root_of_2.poly.gen)  # Should print tan(x), but prints x

root_of_3 = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
print(root_of_3.poly.gen)  # Should print tan(x), but prints x

root_of_4 = RootOf((x**3 + 2*x - 1), 0)
print(root_of_4.poly.gen)  # Should print x, but prints tan(x)

# Check if the issue is fixed
assert root_of_1.poly.gen == x, "RootOf should keep the original generator"
assert root_of_2.poly.gen == symbols('tan(x)'), "RootOf should keep the new generator"
assert root_of_3.poly.gen == symbols('tan(x)'), "RootOf should keep the new generator"
assert root_of_4.poly.gen == x, "RootOf should keep the original generator"

print("Test passed.")
sys.exit(0)
