Here is the reproducer script:

```python
import sympy as sp

def main():
    J = sp.symbols('J')
    m = sp.symbols('m')
    s = sp.symbols('s')

    joule = J*sp.m**2/(sp.s)
    second = sp.s

    try:
        result = sp.convert_to(J*sp.m**2/sp.s, 'joule')
        assert result == J*sp.m**2/sp.s
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

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
    main()
```

This script will run the `convert_to` function with the given inputs and check if the result is equal to the original expression. If it's not, an `AssertionError` will be raised, which will trigger the print_stacktrace function to print the stack trace of the issue.