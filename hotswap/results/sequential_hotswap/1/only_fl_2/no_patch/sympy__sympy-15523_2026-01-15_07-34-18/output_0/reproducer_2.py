import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    line {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_implicit_multiplication_application():
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    
    # Custom transformation setup to include implicit multiplication
    transformations = standard_transformations + (implicit_multiplication_application,)
    
    test_cases = [
        "2sin(x)",
        "2x",
        "sin(x)cos(x)"
    ]
    
    for case in test_cases:
        try:
            # Test parsing each case with transformations applied
            expr = parse_expr(case, transformations=transformations)
            assert expr is not None, "Expression parsing resulted in None."
        except Exception as e:
            print(f"Parse failure on case: '{case}'")
            print_stacktrace(e)
            raise AssertionError("Failed to parse expression with implicit multiplication correctly.")

def test_sympify_keywords():
    from sympy import sympify, SympifyError
    
    # A list of Python keywords to be tested with `sympify`
    keywords = ['if', 'for', 'while', 'lambda']
    
    for keyword in keywords:
        try:
            # Attempt to sympify each Python keyword
            sympify(keyword)
            # If no exception is raised, the test should fail
            raise AssertionError(f"'{keyword}' parsing did not raise SympifyError as expected.")
        except SympifyError:
            pass  # This is the expected path for keywords other than 'lambda'
        except Exception as e:
            print(f"Sympify error with keyword: '{keyword}'")
            print_stacktrace(e)
            raise AssertionError("An unexpected error occurred during `sympify` of a keyword.")

if __name__ == "__main__":
    test_implicit_multiplication_application()
    try:
        test_sympify_keywords()
        print("Issue with 'lambda' keyword has been resolved.")
    except AssertionError as error:
        print_stacktrace(error)
        sys.exit(1)  # Maintain non-zero exit code for unresolved issues
