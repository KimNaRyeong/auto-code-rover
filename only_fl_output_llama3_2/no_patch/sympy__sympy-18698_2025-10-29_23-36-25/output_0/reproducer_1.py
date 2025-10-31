import sympy as sp

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

def reproduce_issue():
    x = sp.symbols('x')
    expression = (x**2 + 1) * ((x - 1)**2 * (x - 2)**3 * (x - 3)**3)
    result = sp.simplify(expression)
    expected_result = ((x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3))
    actual_result = sp.sqf_list(result)

    if actual_result != expected_result:
        raise AssertionError("sqf and sqf_list output is not consistent")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue reproduced successfully.")
    exit(0)
