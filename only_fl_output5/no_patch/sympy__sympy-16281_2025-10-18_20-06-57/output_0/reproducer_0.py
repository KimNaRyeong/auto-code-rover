import sys
from sympy import symbols, oo, Product
from sympy.printing.pretty.pretty import pretty
from sympy.printing.pretty.stringpict import prettyForm

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

def check_format_issue():
    n = symbols('n')
    cases = [
        Product(1, (n, 1, oo)),
        Product(1/n, (n, 1, oo)),
        Product(1/n**2, (n, 1, oo))
    ]

    for case in cases:
        pretty_output = pretty(case, use_unicode=True)
        lines = pretty_output.split('\n')

        # Check for extra empty line at the bottom
        if lines[-1].strip():
            raise AssertionError("Pretty print should not have an extra non-empty line at the bottom.")
        
        # Check for overall shape issues (e.g., too "fat")
        top_line = lines[0]
        bottom_line = lines[-2]  # Considering the actual content before the empty line
        if not (1.5 * len(top_line) >= len(bottom_line) >= len(top_line)):
            raise AssertionError("Pretty print is disproportionately shaped.")

        # Check if extending the top line could solve the issue without making it "ugly"
        len_top = len(top_line.strip())
        len_bottom = len(bottom_line.strip())
        if len_bottom > len_top:
            raise AssertionError("Pretty print needs a better proportioned top line.")

try:
    check_format_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error code to indicate failure

# If no errors, the pretty print issue is considered fixed.
print("No formatting issues detected. Exiting with code 0.")
sys.exit(0)
