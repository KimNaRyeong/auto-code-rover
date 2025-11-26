import sympy

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
    symbol = sympy.Symbol('s')
    assert not hasattr(symbol, '__dict__'), "Symbol instances should not have __dict__"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue is fixed")
    sys.exit(0)
