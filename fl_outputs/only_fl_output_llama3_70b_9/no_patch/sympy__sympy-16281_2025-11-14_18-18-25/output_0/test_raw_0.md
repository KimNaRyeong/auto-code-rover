Here is the `reproducer.py` file that reproduces the issue:
```
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
    (Product(1, (n, 1, oo)), "∞\n┬───┬\n│   │ 1\n│   │\n n = 1"),
    (Product(1/n, (n, 1, oo)), " ∞\n┬──────┬\n│      │ 1\n│      │ ─\n│      │ n\n│      │\n n = 1"),
    (Product(1/n**2, (n, 1, oo)), "   ∞\n┬────────┬\n│        │ 1\n│        │ ──\n│        │  2\n│        │ n\n│        │\n  n = 1"),
    (Product(1, (n, 1, oo)), use_unicode=False, " oo\n_____\n|   | 1\n|   |\n n = 1"),
    (Product(1/n, (n, 1, oo)), use_unicode=False, "  oo\n________\n|      | 1\n|      | -\n|      | n\n|      |\n n = 1"),
    (Product(1/n**2, (n, 1, oo)), use_unicode=False, "   oo\n__________\n|        | 1\n|        | --\n|        |  2\n|        | n\n|        |\n  n = 1")
]

for test_case in test_cases:
    product, expected_output = test_case[:2]
    use_unicode = False if len(test_case) > 2 else True
    output = pprint.pformat(product, use_unicode=use_unicode)
    if output != expected_output:
        raise AssertionError(f"Expected:\n{expected_output}\nGot:\n{output}")
print("All tests passed!")
```
This script defines a list of test cases, each consisting of a `Product` object and the expected pretty-printed output. It then iterates over these test cases, uses `pprint.pformat` to generate the actual output, and raises an `AssertionError` if the actual output does not match the expected output. If all tests pass, it prints "All tests passed!".

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` with a stack trace showing the line numbers of the statements that failed. If the issue is fixed, it will exit with code 0 and print "All tests passed!".