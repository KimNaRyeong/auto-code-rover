import sympy
from sympy import symbols

def main():
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)

    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

    result1 = bug.subs(a, 1).apart()
    result2 = bug.apart(t)

    assert str(result1) == "-t + 1/2 - 1/(2*(2*t - 1))", f"Expected '-t + 1/2 - 1/(2*(2*t - 1))' but got {result1}"
    assert str(result2) != "-a*t", f"Expected result to be different from '-a*t' but got {result2}"

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
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
