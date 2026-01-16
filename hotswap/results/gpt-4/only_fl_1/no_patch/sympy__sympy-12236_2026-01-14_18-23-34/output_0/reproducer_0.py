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

    expected_result = bug.subs(a, 1).apart()
    actual_result = bug.apart(t)

    # The expected behavior is that the expression simplification should be consistent
    # regardless of parameter substitution before or after calling `apart()`.
    # The test checks if the inconsistency reported in the issue still exists.
    try:
        assert str(expected_result) == str(actual_result), "Inconsistency detected in expression simplification"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate failure
    else:
        print("Issue has been resolved.")
        exit(0)

if __name__ == "__main__":
    main()
