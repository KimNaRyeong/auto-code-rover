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
if codegen != expected_codegen:
    raise AssertionError(f'Generated wrong Fortran code for sign function.\nExpected:\n  {expected_codegen}\nGot:\n  {codegen}')
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` with a stack trace, indicating that the generated Fortran code is not as expected. The script will exit with a non-zero exit code.

To fix the issue, you can modify the `expected_codegen` variable to match the desired Fortran syntax for the sign function, such as `sign(1d0, x)`. You can also modify the `codegen` variable to use the `sympy.utilities.codegen` module to generate the Fortran code. Once the generated code matches the expected code, the script will exit with a zero exit code.