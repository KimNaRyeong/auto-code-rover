# reproducer.py
def test_implicit_multiplication_application():
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
    transformations = (standard_transformations + (implicit_multiplication_application,))
    # Case that should cause the problem
    test_cases = [
        "factorial()",
        "x factorial()"
    ]
    for case in test_cases:
        try:
            # This will raise an exception if the issue is present
            parse_expr(case, transformations=transformations)
        except Exception as e:
            raise AssertionError("Failed on case: {}".format(case)) from e

def test_sympify_keywords():
    from sympy import sympify, SympifyError

    keywords = ['if', 'for', 'while', 'lambda']
    for kw in keywords:
        try:
            # This should raise an exception for each keyword
            sympify(kw)
        except SympifyError:
            continue
        except Exception as e:
            raise AssertionError("Failed on keyword: {}".format(kw)) from e
    else:
        # If no exception was raised for 'lambda', assert
        if 'lambda' in keywords:
            raise AssertionError("Did not raise SympifyError for 'lambda'.")

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
    try:
        test_implicit_multiplication_application()
        test_sympify_keywords()
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    print("If this message is printed, the issues are either fixed or could not be reproduced.")
