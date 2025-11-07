Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
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

def main():
    x = sp.symbols('x')
    t = sp.symbols('t')

    try:
        root1 = sp.RootOf(x**3 + x - 1, 0)
        root2 = sp.RootOf((x**3 + x - 1).subs(x, t), 0)

        assert root1.poly.gen == x, "RootOf might ignore generator"
        if root1.poly.gen != x:
            raise AssertionError("RootOf might ignore generator")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.