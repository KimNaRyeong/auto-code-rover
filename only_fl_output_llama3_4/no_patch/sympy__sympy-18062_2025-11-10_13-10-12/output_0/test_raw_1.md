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
        imageset = sp.imageset(Lambda(lambda n: 1 + I*n), sp.Integers)
        if not isinstance(imageset, set):
            raise AssertionError("Expected a set but got {}".format(type(imageset)))
        result = str(imageset)
        if "ⅈ⋅n | n ∊ ℤ" not in result:
            raise AssertionError("Expected output 'ⅈ⋅n | n ∊ ℤ' but got {}".format(result))
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create an `imageset` with the given lambda function and integers. If the issue is present, it will raise an `AssertionError`, which will be caught by the script and printed along with a stack trace. The script will then exit with code 1.