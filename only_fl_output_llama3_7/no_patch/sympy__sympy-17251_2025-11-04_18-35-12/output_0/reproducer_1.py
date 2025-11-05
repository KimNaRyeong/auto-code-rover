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
        exp_result = sp.exp(9*sp.I*sp.pi/4)
        simplify_result = sp.simplify(exp_result)
        assert simplify_result != exp_result, "exp doesn't simplify based on its periodicity"
        a = exp_result - sp.exp(sp.I*sp.pi/4)
        print(a)
        simplify_a = sp.simplify(a)
        print(simplify_a)
        expand_complex_a = sp.expand_complex(a)
        print(expand_complex_a)
        assert expand_complex_a != 0, "exp doesn't simplify based on its periodicity"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
