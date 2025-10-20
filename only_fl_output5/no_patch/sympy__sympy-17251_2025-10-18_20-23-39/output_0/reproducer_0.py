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

def test_simplify_exp():
    from sympy import exp, I, pi, simplify, expand_complex

    # Test case where exp does not simplify based on its periodicity
    original_expression = exp(9*I*pi/4)
    simplified_expression = simplify(exp(9*I*pi/4))
    
    # Expecting the simplified expression to not match original due to periodicity
    try:
        assert simplified_expression != original_expression, "Simplified expression should be different due to periodicity"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    # Additional test where the periodicity should lead to simplification
    expression = exp(9*I*pi/4) - exp(I*pi/4)
    simplified = simplify(expression)
    expanded_complex = expand_complex(expression)
    
    try:
        assert simplified == expanded_complex, "Simplified expression and expanded complex form do not match"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_simplify_exp()
        print("Test passed: Issue with exp simplification based on its periodicity seems to be resolved.")
    except AssertionError:
        # If AssertionError occurred, the issue is present.
        exit(1)
