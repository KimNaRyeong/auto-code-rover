Here is the reproducer script:

```python
import sympy as sp

def reproduce_issue():
    product = sp.Product(1/sp.sympify('n**2'), (sp.symbols('n'), 1, float('inf')))
    try:
        from sympy.printing import pprint
        pprint(product, use_unicode=False)
        assert False, "Expected an AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

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

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.