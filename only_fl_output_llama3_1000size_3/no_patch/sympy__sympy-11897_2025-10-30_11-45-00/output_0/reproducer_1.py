import sympy as sp

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
        x = sp.var('x', positive=True)
        latex_expr = str(sp.latex(x*sp.exp(-x)*sp.log(x)))
        pretty_printed_expr = str(sp.pretty_print(x*sp.exp(-x)*sp.log(x)))
        
        if latex_expr != pretty_printed_expr:
            raise AssertionError("LaTeX printer is inconsistent with pretty printer")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
