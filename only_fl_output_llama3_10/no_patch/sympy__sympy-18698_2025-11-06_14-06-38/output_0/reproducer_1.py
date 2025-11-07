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
    try:
        x = sp.symbols('x')
        expression = sp.sympify("(x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3")
        result = sp.sqf_list(expression)
        if result != (1, [(sp.Pow(x**2 + 1, 1), 1), (sp.Pow(x - 1, 2), 1), (sp.Pow(x - 2, 3), 1), (sp.Pow(x - 3, 3), 1)]):
            raise AssertionError("Expected output not matched")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
