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

def test_sympy_latex_issue():
    from sympy import symbols, latex, acsc

    x = symbols('x')
    try:
        # This should work as expected for full inverse trig function names.
        result_acsc = latex(acsc(x), inv_trig_style="full")
        assert result_acsc == '\\arccsc{\\left (x \\right )}', "Incorrect latex for acsc with full inverse trig style"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Using exit code 1 to indicate failure due to AssertionError

if __name__ == "__main__":
    test_sympy_latex_issue()
    print("No issue detected.")  # This will only execute if the assertion does not fail
    exit(0)
