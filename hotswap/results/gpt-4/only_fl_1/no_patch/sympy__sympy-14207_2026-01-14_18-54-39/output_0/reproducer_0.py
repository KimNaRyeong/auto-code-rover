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

def check_issue():
    from sympy import Symbol, Pow, Mul
    
    a = Symbol('a')
    u = Symbol('u')
    
    a2inv = Pow(Mul(a, a, evaluate=False), -1, evaluate=False)
    d = Mul(-2, u, a2inv, evaluate=False)
    
    correct_output = "-2*u/(a*a)"
    obtained_output = str(d)
    
    assert obtained_output == correct_output, f"Expected output: {correct_output}, but got: {obtained_output}"

if __name__ == "__main__":
    try:
        check_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1) # Exit with a non-zero code to indicate failure
    else:
        print("No issue detected.")
        exit(0)
