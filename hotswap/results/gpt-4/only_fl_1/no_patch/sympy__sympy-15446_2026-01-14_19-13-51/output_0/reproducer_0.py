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

def main():
    try:
        from sympy import MatrixSymbol, latex

        x = MatrixSymbol('x', 2, 2)
        y = MatrixSymbol('y', 2, 2)
        expr = (x*y).subs(y, -y)
        result = latex(expr)

        # Check if the issue is present
        expected = 'x \\left(- y\\right)'  # Put the expected output here considering the issue is fixed
        if result != expected:
            raise AssertionError(f"LaTeX printer omits necessary parentheses. Expected '{expected}', got '{result}'")
    
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate an issue present

    print("Issue fixed.")
    exit(0)

if __name__ == "__main__":
    main()
