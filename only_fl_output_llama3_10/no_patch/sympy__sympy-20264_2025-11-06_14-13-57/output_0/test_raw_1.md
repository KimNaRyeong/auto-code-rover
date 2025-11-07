Here is the reproducer script:

```python
import sympy as sp

def main():
    try:
        expr = sp.Pow(sp.Rational(1, 2), -1, evaluate=False)
        latex_expr = str(sp.latex(expr))
        print(latex_expr)
    except RecursionError as e:
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

        print_stacktrace(e)
        raise AssertionError("RecursionError occurred")

if __name__ == "__main__":
    main()
```

This script creates a `Pow` expression with a rational number and an exponent of -1, then attempts to convert it to LaTeX. If the conversion raises a `RecursionError`, the script prints the stack trace using the provided function and raises an `AssertionError`.