# reproducer.py

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
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication_application,
    )
    from sympy import simplify
    
    transformations = (standard_transformations + (implicit_multiplication_application,))

    # Parsing expressions with and without custom transformations
    expr1 = parse_expr('2**n * 3**n')
    expr2 = parse_expr('2**n3**n', transformations=transformations)

    # Attempt to simplify the difference between the two expressions
    simplified_diff = simplify(expr1 - expr2)

    # Check if the simplified difference is not equal to zero, indicating an issue
    if simplified_diff != 0:
        raise AssertionError(f"Expected 0, but got {simplified_diff}")

except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("Issue resolved.")
    SystemExit(0)
