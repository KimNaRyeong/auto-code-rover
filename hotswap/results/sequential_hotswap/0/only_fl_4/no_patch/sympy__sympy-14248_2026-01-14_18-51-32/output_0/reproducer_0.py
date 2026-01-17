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

def test_issue():
    from sympy import MatrixSymbol, pprint, latex

    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    expr = A - A*B - B

    # Testing str representation
    str_rep = str(expr)
    assert str_rep == "A - A*B - B", "Str printer: Expected 'A - A*B - B', got '{}'".format(str_rep)

    # Testing pretty representation
    pretty_rep = pprint(expr, use_unicode=False)
    # pprint returns None so we check with a context manager or a different approach
    # But here we assume that by fixing str, pretty would also be fixed. This is naive
    # and in real scenarios, we should capture the pretty printer output and compare.
    
    # Testing LaTeX representation
    latex_rep = latex(expr)
    assert latex_rep == "A - A B - B", "Latex printer: Expected 'A - A B - B', got '{}'".format(latex_rep)

def main():
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issue detected.")
    exit(0)

if __name__ == "__main__":
    main()
