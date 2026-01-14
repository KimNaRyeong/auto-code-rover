 Here's a reproducer script that demonstrates the issue with `simplify` in `Integral`:

```python
from sympy import Integral, simplify, examples
from sympy.abc import x, y, n, z

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# The issue is present in this line
assert simplify(Integral(x*y, (x, 1, n))) != Integral(simplify(x*y), (x, 1, n)), "simplify does not pull out the constant term in Integral"

# This line should not be executed when the issue is present
print("The issue is fixed.")
```

To reproduce the issue, save the above code in a file named `reproducer.py` in the root directory of the Sympy project and execute it with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace showing the line where the issue is present.

When the issue is fixed, the script should print "The issue is fixed." and exit with code 0.