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

expected_output1 = "∞\n┬───┬\n│   │ 1\n│   │\n n = 1"
expected_output2 = " ∞\n┬──────┬\n│      │ 1\n│      │ ─\n│      │ n\n│      │\n n = 1"
expected_output3 = "   ∞\n┬────────┬\n│        │ 1\n│        │ ──\n│        │  2\n│        │ n\n│        │\n  n = 1"

output1 = pprint.pformat(product1, width=20)
output2 = pprint.pformat(product2, width=20)
output3 = pprint.pformat(product3, width=20)

if output1 != expected_output1:
    raise AssertionError(f"Expected:\n{expected_output1}\nGot:\n{output1}")
if output2 != expected_output2:
    raise AssertionError(f"Expected:\n{expected_output2}\nGot:\n{output2}")
if output3 != expected_output3:
    raise AssertionError(f"Expected:\n{expected_output3}\nGot:\n{output3}")

print("All tests passed!")
