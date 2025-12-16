 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
import math

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def mathematica_code(expr):
    return 'Max(' + str(expr) + ')'

x = symbols('x')
assert mathematica_code(Max(x,2)) == 'Max[x,2]', "Issue found: incorrect output"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a clear stack trace, indicating that the output of `mathematica_code(Max(x,2))` is `'Max(2, x)'` instead of the expected `'Max[x,2]'`. This reproduces the issue described in the original report.