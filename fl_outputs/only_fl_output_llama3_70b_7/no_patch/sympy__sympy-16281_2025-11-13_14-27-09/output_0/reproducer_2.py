import pprint
from sympy import Symbol, oo, Product

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

product1 = Product(1, (n, 1, oo))
product2 = Product(1/n, (n, 1, oo))
product3 = Product(1/n**2, (n, 1, oo))

try:
    pprint.pprint(product1, width=100)
    assert '∞\n┬───┬' in str(pprint.pformat(product1)), "Pretty print of product is not as expected"
    pprint.pprint(product2, width=100)
    assert '∞\n┬──────┬' in str(pprint.pformat(product2)), "Pretty print of product is not as expected"
    pprint.pprint(product3, width=100)
    assert '∞\n┬────────┬' in str(pprint.pformat(product3)), "Pretty print of product is not as expected"
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("All test cases passed!")
