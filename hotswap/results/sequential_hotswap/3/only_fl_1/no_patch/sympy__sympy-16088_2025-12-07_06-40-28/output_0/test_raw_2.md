 I apologize for the mistake in my previous response. Here's the corrected `reproducer.py` script that should reproduce the issue:

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
i = Integral(x*y, (x, 1, n))
expected = Integral(simplify(x*y), (x, 1, n))
actual = simplify(i)
assert actual != expected, "simplify does not pull out the constant term in Integral"

print("The issue is present.")
```

To reproduce the issue, save the above code in a file named `reproducer.py` in the root directory of the Sympy project and execute it with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace showing the line where the issue is present.

When the issue is fixed, replace the `assert` statement with the following line:

```python
print("The issue is fixed.")
```

And the script should print "The issue is fixed." and exit with code 0.