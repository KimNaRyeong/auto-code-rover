import sympy as sp
from sympy.abc import x

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

def test_root_of_ignores_generator():
    try:
        # First case
        root_of_original = sp.RootOf(x**3 + x - 1, 0)
        root_of_substituted = sp.RootOf((x**3 + x - 1).subs(x, sp.tan(x)), 0)
        assert root_of_substituted.poly.gen == sp.tan(x), "Generator should be tan(x) but got {}".format(root_of_substituted.poly.gen)

        # Second case
        root_of_new_form = sp.RootOf(sp.tan(x)**3 + 2 * sp.tan(x) - 1, 0)
        root_of_same_form_new_generator = sp.RootOf((x**3 + 2 * x - 1), 0)
        assert root_of_same_form_new_generator.poly.gen == x, "Generator should be x but got {}".format(root_of_same_form_new_generator.poly.gen)

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # If the issue is present, exit with an error
    else:
        print("No issues found, the generators are handled correctly.")
        exit(0)

if __name__ == "__main__":
    test_root_of_ignores_generator()
