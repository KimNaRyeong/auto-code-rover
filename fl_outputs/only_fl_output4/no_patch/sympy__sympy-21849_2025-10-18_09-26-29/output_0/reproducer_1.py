# reproducer.py
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

def sympy_latex_rendering_check():
    """Mimics the LaTeX rendering part of _repr_latex_ for SymPy objects"""
    sp.init_printing(use_latex='mathjax')
    expr = sp.Pow(sp.LambertW(2), 2)
    latex_string = sp.latex(expr)
    print(latex_string)
    
def main():
    try:
        sympy_latex_rendering_check()
        print("The issue is fixed, exiting with code 0.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue with displaying LambertW raised to a power is present.")

if __name__ == "__main__":
    main()
