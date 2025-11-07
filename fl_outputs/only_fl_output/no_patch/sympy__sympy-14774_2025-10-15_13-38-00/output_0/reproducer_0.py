from sympy import symbols, acsc, latex
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')

try:
    # This should return '\\operatorname{arccsc}{\\left (x \\right )}' when the issue is fixed.
    result = latex(acsc(x), inv_trig_style="full")
    assert result == '\\arccsc{\\left (x \\right )}', f"Expected '\\arccsc{{\\left (x \\right )}}', got '{result}'"
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with a non-zero code to indicate an error has occurred.

# If execution reaches this point, it means the issue has likely been fixed.
print("Issue not detected, exiting normally.")
sys.exit(0)
