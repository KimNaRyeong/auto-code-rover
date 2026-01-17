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
    from sympy import MatrixSymbol, pprint, latex
    
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    
    expression = A - A*B - B
    
    expected_str_output = 'A - A*B - B'
    expected_pprint_output = '-A⋅B + A - B' # Note: pprint output expectations might need adjustments
    expected_latex_output = 'A - A B - B' # Note: the LaTeX assertion might be too strict; adjust as needed

    # Testing str output
    str_output = str(expression)
    assert expected_str_output in str_output, f"Incorrect str output: {str_output}"

    # Testing pprint output
    from io import StringIO
    import sys
    buffer = StringIO()
    sys.stdout = buffer
    pprint(expression, use_unicode=True)
    sys.stdout = sys.__stdout__
    pprint_output = buffer.getvalue().strip()
    assert expected_pprint_output in pprint_output, f"Incorrect pprint output: {pprint_output}"

    # Testing latex output
    latex_output = latex(expression)
    assert expected_latex_output in latex_output, f"Incorrect latex output: {latex_output}"

    # If none of the assertions fail, then the issue is considered fixed
    print("Issue fixed.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
