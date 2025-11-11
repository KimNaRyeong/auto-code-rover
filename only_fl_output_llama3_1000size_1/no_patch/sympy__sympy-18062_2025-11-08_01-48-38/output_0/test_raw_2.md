Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import I

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

def reproduce_issue():
    try:
        from sympy import Lambda, Integers
        imageset = sp.imageset(Lambda(n, 1 + I*n), Integers)
        if str(imageset) != "{ⅈ⋅n | n ∊ ℤ}":
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by calling `sp.imageset(Lambda(n, 1 + I*n), Integers)`. If the issue is present (i.e., the output does not equal "{ⅈ⋅n | n ∊ ℤ}"), it will raise an `AssertionError` and print a stack trace.