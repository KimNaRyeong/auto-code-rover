import pprint
from sympy import Symbol, oo

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

n = Symbol('n')

# Test cases
test_cases = [
    (1, (n, 1, oo)),
    (1/n, (n, 1, oo)),
    (1/n**2, (n, 1, oo))
]

for test_case in test_cases:
    product = test_case[0] * test_case[1][0]**test_case[1][1] * test_case[1][2]
    try:
        output = pprint.pformat(product)
        assert "∞" in output and "\n┬───┬\n" in output, "Expected different output"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

exit(0)
