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

def reproduce_issue_with_implicit_multiplication_application():
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    try:
        # Attempt to parse an expression that should lead to the described error if the issue is present
        parse_expr("2*factorial(2)", transformations=(standard_transformations + (implicit_multiplication_application,)))
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected exception during implicit multiplication parsing."

def reproduce_issue_with_sympify():
    from sympy import sympify, SympifyError
    try:
        sympify('lambda', evaluate=False)
        # If no exception is raised, the expected issue is not present; raise AssertionError
        assert False, "Expected SympifyError not raised for 'lambda'."
    except SympifyError:
        # Expected; do nothing as this is the correct behavior
        pass
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected exception type encountered."

if __name__ == "__main__":
    try:
        reproduce_issue_with_implicit_multiplication_application()
        reproduce_issue_with_sympify()
        print("No AssertionError raised. The issues seem to be fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with non-zero to indicate the presence of the issue
