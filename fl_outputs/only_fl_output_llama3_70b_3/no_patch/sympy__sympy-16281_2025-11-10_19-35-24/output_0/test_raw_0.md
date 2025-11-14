Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
```python
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
    (Product(1, (n, 1, oo)), "∞\n┬───┬\n│   │ 1\n│   │\nn = 1"),
    (Product(1/n, (n, 1, oo)), " ∞\n┬──────┬\n│      │ 1\n│      │ ─\n│      │ n\n│      │\nn = 1"),
    (Product(1/n**2, (n, 1, oo)), "   ∞\n┬────────┬\n│        │ 1\n│        │ ──\n│        │  2\n│        │ n\n│        │\nn = 1"),
    (Product(1, (n, 1, oo)), False, " oo\n_____\n|   | 1\n|   |\nn = 1"),
    (Product(1/n, (n, 1, oo)), False, "  oo\n________\n|      | 1\n|      | -\n|      | n\n|      |\nn = 1"),
    (Product(1/n**2, (n, 1, oo)), False, "   oo\n__________\n|        | 1\n|        | --\n|        |  2\n|        | n\n|        |\nn = 1"),
]

for test_case in test_cases:
    product, *args = test_case
    expected_output = test_case[1]
    use_unicode = True if len(args) == 1 else args[1]
    try:
        output = pprint.pformat(product, use_unicode=use_unicode)
        assert output.strip() == expected_output, f"Expected:\n{expected_output}\nGot:\n{output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

print("All test cases passed!")
```
This script will reproduce the issue and raise an `AssertionError` if the pretty printing of `Product` does not match the expected output. If all test cases pass, it will exit with code 0.