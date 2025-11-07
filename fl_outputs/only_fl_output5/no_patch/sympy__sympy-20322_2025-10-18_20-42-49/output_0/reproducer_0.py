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

def test_sympify_simplify_behavior():
    try:
        # The expressions being tested
        expr_with_evaluate_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
        expr_with_evaluate_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

        # Checking if both expressions yield the same output
        assert expr_with_evaluate_false == expr_with_evaluate_true, "Inconsistent behaviour with ceiling function"

        print("Test passed: The behavior is consistent across evaluate=True and evaluate=False.")

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_sympify_simplify_behavior()
