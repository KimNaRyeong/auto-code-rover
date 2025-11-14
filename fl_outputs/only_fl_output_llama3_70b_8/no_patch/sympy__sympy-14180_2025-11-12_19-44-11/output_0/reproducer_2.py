import sympy as sp

def latex_converter(math_expression):
    return sp.latex(math_expression)

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
    try:
        expression = sp.sympify('ln(10)')
        converted_latex = latex_converter(expression)
        assert 'ln' in converted_latex, "Expected 'ln' in the LaTeX output but got {}".format(converted_latex)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
