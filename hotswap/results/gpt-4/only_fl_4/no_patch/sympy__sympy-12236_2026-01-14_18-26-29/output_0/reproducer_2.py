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
    from sympy import symbols

    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)

    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

    subs_bug = bug.subs(a, 1)
    apart_subs_bug = subs_bug.apart()
    apart_bug = bug.apart(t)

    try:
        assert str(apart_subs_bug) != "-t + 1/2 - 1/(2*(2*t - 1))", "Substituted then apart() result matches the unexpected output"
        assert str(apart_bug) != "-a*t", "apart() directly result matches the unexpected output"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 because the issue is present.

    # If no issue, exit cleanly
    print("No issue detected.")
    exit(0)

if __name__ == "__main__":
    main()
