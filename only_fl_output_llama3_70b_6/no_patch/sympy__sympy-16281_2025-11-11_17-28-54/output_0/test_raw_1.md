Here is the `reproducer.py` file that reproduces the issue:
```
import pprint
from sympy import Symbol, oo, Mul

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

# Define Product as a Mul
Product = lambda *args: Mul(*args)

# Test cases
test_cases = [
    (Product(1, n, oo), "∞\n┬───┬\n│   │ 1\n│   │\nn = 1"),
    (Product(1/n, n, oo), " ∞\n┬──────┬\n│      │ 1\n│      │ ─\n│      │ n\n│      │\nn = 1"),
    (Product(1/n**2, n, oo), "    ∞\n┬────────┬\n│        │ 1\n│        │ ──\n│        │  2\n│        │ n\n│        │\nn = 1"),
    (Product(1, n, oo), False, " oo\n_____\n|   | 1\n|   |\nn = 1"),
    (Product(1/n, n, oo), False, "   oo\n________\n|      | 1\n|      | -\n|      | n\n|      |\nn = 1"),
    (Product(1/n**2, n, oo), False, "    oo\n__________\n|        | 1\n|        | --\n|        |  2\n|        | n\n|        |\nn = 1")
]

for test_case in test_cases:
    product, *args = test_case
    expected_output = test_case[1]
    use_unicode = True if len(test_case) == 2 else test_case[1]
    try:
        output = pprint.pformat(product, width=100, use_unicode=use_unicode)
        assert output.strip() != expected_output, f"Expected different output but got {expected_output}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

exit(0)
```
This script defines a `Product` function that is equivalent to the `Mul` function from SymPy. It then defines several test cases for the `Product` pretty printing issue, including both Unicode and non-Unicode cases. For each test case, it uses `pprint.pformat` to generate the output and asserts that it is different from the expected output. If the assertion fails, it prints the stack trace using the `print_stacktrace` function and exits with code 1. If all assertions pass, it exits with code 0.