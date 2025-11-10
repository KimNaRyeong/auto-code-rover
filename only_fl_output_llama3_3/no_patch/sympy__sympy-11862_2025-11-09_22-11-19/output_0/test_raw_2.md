Here is the reproducer script:

```python
import sympy as sp
import mpmath as mp
from sympy.utilities.lambdify import lambdify

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
    g = sp.sqrt(2) - x
    h = g.evalf(64)

    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')

    try:
        result1 = f1(mp.mpf('0'))
        result2 = f2(mp.mpf('1.414213562373095048801688724209698078569671875376948073176679738'))
    except Exception as e:
        print_stacktrace(e)
        raise

    if not (result1 == mp.mpf('-0 + 1.414213562373095048801688724209698078569671875376948073176679738') and result2 == mp.mpf('0')):
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script will run the lambdification of `g` and `h`, then call these functions with specific inputs. If the issue is present, it will print the stack trace and raise an `AssertionError`.