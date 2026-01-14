 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp
from sympy.abc import x

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

expected_codegen = 'sign(1, x)'
codegen = sp.fcode(sp.sign(x))
assert codegen == expected_codegen, f"Expected: {expected_codegen}, Got: {codegen}"
```
To run the script, execute `python3 reproducer.py`. The script should raise an `AssertionError` with a stack trace, showing that the generated Fortran code is not as expected.

To fix the issue, you can modify the `expected_codegen` variable to match the desired Fortran syntax for the sign function, such as `sign(1d0, x)`. You can also modify the Sympy code to generate the desired Fortran syntax for the sign function. Once the issue is fixed, the script should exit with code 0.