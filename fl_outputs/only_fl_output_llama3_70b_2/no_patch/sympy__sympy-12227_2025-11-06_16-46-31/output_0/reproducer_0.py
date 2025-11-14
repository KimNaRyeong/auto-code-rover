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

try:
    from sympy import Float

    # Create a float with 54 binary digits
    f = Float(1.0, 17)  # This will set prec to 56, not 54

    # Check if the precision is correct
    assert f._prec == 54, "Float constructor does not allow setting binary precision"

    print("Issue fixed!")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
