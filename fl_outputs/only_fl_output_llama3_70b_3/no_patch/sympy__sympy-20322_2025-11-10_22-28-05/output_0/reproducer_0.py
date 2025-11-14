import sympy

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

def main():
    x = sympy.symbols('x')
    
    # Reproduce the issue
    expr1 = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
    simplified_expr1 = expr1.simplify()
    expected_result1 = '4*ceiling(x/4 - 3/4)'
    if str(simplified_expr1) != expected_result1:
        raise AssertionError(f"Inconsistent behavior for sympify/simplify with ceiling. Expected {expected_result1}, got {simplified_expr1}")
    
    expr2 = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True)
    simplified_expr2 = expr2.simplify()
    expected_result2 = '4*ceiling(x/4 - 3/4)'
    if str(simplified_expr2) != expected_result2:
        raise AssertionError(f"Inconsistent behavior for sympify/simplify with ceiling. Expected {expected_result2}, got {simplified_expr2}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
