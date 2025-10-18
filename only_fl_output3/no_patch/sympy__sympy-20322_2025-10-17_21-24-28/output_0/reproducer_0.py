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

def test_sympify_simplify_with_ceiling():
    # Define expressions
    expression_1 = '4*ceiling(x/4 - 3/4)'
    
    # Test for sympy version 1.6.2 behavior
    try:
        # Case with evaluate=False
        result_1 = sympy.sympify(expression_1, evaluate=False).simplify()
        # Case with evaluate=True
        result_2 = sympy.sympify(expression_1, evaluate=True).simplify()
        
        # Asserting both cases to ensure consistency
        assert str(result_1) == str(result_2), "Inconsistent simplification with ceiling and evaluate flag"
    
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Raise the AssertionError to indicate failure in consistency

if __name__ == "__main__":
    test_sympify_simplify_with_ceiling()  # Run the test

