# reproducer.py
from sympy import symbols, Product, oo
from sympy.printing.pretty.pretty import pprint
import io
import sys

def capture_pretty(obj, **kwargs):
    """Utility function to capture sympy's pretty print output."""
    old_stdout = sys.stdout
    result = io.StringIO()
    sys.stdout = result
    pprint(obj, **kwargs)
    sys.stdout = old_stdout
    return result.getvalue()

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

def check_product_pretty_print():
    n = symbols('n')
    tests = [
        (Product(1, (n, 1, oo)), True),
        (Product(1/n, (n, 1, oo)), True),
        (Product(1/n**2, (n, 1, oo)), True),
        (Product(1, (n, 1, oo)), False),
        (Product(1/n, (n, 1, oo)), False),
        (Product(1/n**2, (n, 1, oo)), False),
    ]
    for product, use_unicode in tests:
        output = capture_pretty(product, use_unicode=use_unicode)
        try:
            # Check for extra empty line
            assert not output.endswith('\n\n'), "Extra empty line at the bottom of the product"
            # Check the width of the ∏ or Prod based on unicode usage
            lines = output.split('\n')
            if use_unicode:
                # Assuming improvements made here are specific, adjust as necessary
                assert len(lines[1]) <= 7, "∏ is too fat"  # This condition is arbitrary; adjust based on expected improvements
            else:
                # Check that ASCII version aligns with expectations; this is arbitrary and should be adjusted.
                assert len(lines[1]) <= 8, "Prod is too fat"  # This condition is arbitrary; adjust based on expected improvements
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == "__main__":
    try:
        check_product_pretty_print()
        print("No issue detected with Product pretty print.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
