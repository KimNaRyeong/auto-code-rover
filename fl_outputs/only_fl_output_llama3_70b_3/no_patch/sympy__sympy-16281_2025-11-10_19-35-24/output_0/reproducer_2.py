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

output1 = pprint.pformat(product1)
output2 = pprint.pformat(product2)
output3 = pprint.pformat(product3)

# Check if there is an empty line at the bottom of the output
if output1.strip().endswith('\n') or output2.strip().endswith('\n') or output3.strip().endswith('\n'):
    raise AssertionError("There is an empty line at the bottom of the output")

# Check if the ∏ is too fat
if '∞' in output1 and len([c for c in output1 if c == '∞']) > 1:
    raise AssertionError("The ∏ is too fat")
elif 'oo' in output1 and len([c for c in output1 if c == 'o']) > 2:
    raise AssertionError("The oo is too fat")

print("All test cases passed!")
