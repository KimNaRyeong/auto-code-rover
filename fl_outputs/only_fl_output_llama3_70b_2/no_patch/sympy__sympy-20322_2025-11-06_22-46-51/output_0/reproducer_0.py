import sympy

def test_sympify(evaluate):
    expr = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=evaluate)
    simplified_expr = expr.simplify()
    expected_expr = '4*ceiling(x/4 - 3/4)'
    if str(simplified_expr) != expected_expr:
        raise AssertionError(f"Inconsistent behavior for sympify/simplify with ceiling. Expected {expected_expr}, got {simplified_expr}")

def main():
    try:
        test_sympify(evaluate=False)
        test_sympify(evaluate=True)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
