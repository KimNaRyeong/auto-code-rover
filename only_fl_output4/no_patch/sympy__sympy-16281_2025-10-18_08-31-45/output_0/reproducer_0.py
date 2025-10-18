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
    from sympy import symbols, Product, oo
    from sympy.printing.pretty.pretty import pretty

    n = symbols('n')
    expected_output = """
    ∞
─┬─────┬─
 │     │  1
 │     │  ──
 │     │   2
 │     │  n
  n = 1
""".strip()

    # Check pretty print for Product(1/n**2, (n, 1, oo)) without extra line and with a thinner frame
    actual_output = pretty(Product(1/n**2, (n, 1, oo)), use_unicode=True).strip()

    # Assertion to verify the pretty print output matches expected improvements
    try:
        assert actual_output == expected_output, "Pretty print output does not match expected improvements."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate the presence of the issue
    else:
        print("Issue resolved. Exiting with code 0.")
        exit(0)  # Exit with code 0 to indicate the issue is fixed

if __name__ == "__main__":
    main()
