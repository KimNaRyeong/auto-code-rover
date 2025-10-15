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
    import sympy as sp
    sp.init_printing(use_latex='mathjax')

    # Dummy symbols and sequence definition
    n = sp.symbols('n', integer=True)
    seq = sp.SeqFormula(n**2, (n, 0, sp.oo))

    # Attempt to reproduce the issue by evaluating the LaTeX string representation
    # Although this does not mimic the Jupyter rendering, it's a proxy to catch potential issues.
    latex_str = sp.latex(seq)

    try:
        # Assert that backslash-escaped square brackets are not present in the LaTeX string
        assert '\\left\\[' not in latex_str and '\\right\\]' not in latex_str
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)
