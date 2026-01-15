To create a standalone Python file that reproduces the original issue presented, which involves incorrect behavior of the `simplify` function in SymPy, we'll focus specifically on the problem described involving polynomial factorization and simplification. Given the broad nature of the issues (incorrect factorization and unexpected results with `simplify`), the reproducer below addresses the polynomial issue specifically, as it presents a clear mathematical inconsistency that can be programmatically checked.

```python
# reproducer.py
import sympy as sp

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

def test_polynomial_factorization():
    x, y = sp.symbols('x y')
    z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
    w = sp.expand(z)
    v = sp.factor(w)
    expanded_v = sp.expand(v)

    # Check if the expanded factorized form matches the original expanded form
    try:
        assert sp.simplify(expanded_v - w) == 0, "Factorization and re-expansion resulted in different expression!"
    except AssertionError as e:
        print("Issue found in polynomial factorization:")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    try:
        test_polynomial_factorization()
        print("No issue found, polynomial factorization works as expected.")
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        exit(1)
    exit(0)
```

Place this script in the root directory and run it with Python 3. This script:

1. Defines a polynomial expression that is expected to trigger the issue based on the details provided.
2. Expands, factors, and then re-expands the expression to check for inconsistencies.
3. Asserts that the re-expanded form should match the originally expanded form, indicating correct factorization.
4. Uses the provided `print_stacktrace` function to display detailed error information if the assertion fails.
   
This approach aims to provide a straightforward reproducer for the specific case of polynomial factorization and expansion, reflecting the initial problem discussed. When the issue is present, the script will exit with code 1 and print a detailed stack trace. If the underlying issue with `simplify` or `factor` is resolved in a future version of SymPy, running this script should show no errors and exit with code 0, indicating that the problem has been fixed.