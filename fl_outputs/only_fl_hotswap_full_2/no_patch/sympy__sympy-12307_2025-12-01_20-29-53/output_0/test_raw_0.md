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
To run the script, execute `python3 reproducer.py` in the terminal. The script should raise an `AssertionError` with a stack trace showing the line number of the statement that failed the assertion. The expected and actual output of the `sp.fcode(sp.sign(x))` call are also shown in the error message.

The script exits with a non-zero exit code (1) when the issue is present, indicating that the script failed. When the issue is fixed, the script should exit with a zero exit code (0), indicating that the script succeeded.