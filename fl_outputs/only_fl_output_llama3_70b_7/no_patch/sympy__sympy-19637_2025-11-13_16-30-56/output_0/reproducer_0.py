import sympy
from sympy.core.sympify import kernS

def reproduce_issue():
    text = "(2*x)/(x-1)"
    try:
        expr = kernS(text)  
        hit = kern in s  # This line should raise an UnboundLocalError
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue is present"

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
    reproduce_issue()
