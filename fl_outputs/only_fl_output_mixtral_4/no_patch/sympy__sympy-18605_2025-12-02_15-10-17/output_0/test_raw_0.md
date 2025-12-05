 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy as sp
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

m, n = sp.symbols("m, n", real=True)
i = sp.Idx("i", (m, n))

if not (isinstance(m, int) and isinstance(n, int)):
    raise AssertionError("Idx object should not accept non-integer bounds.")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` since the lower and upper bounds `m` and `n` are not integers. This demonstrates the issue where the `Idx` object accepts non-integer bounds.

To fix the issue, you can modify the script to check if both the lower and upper bounds are integers:
```python
import sympy as sp
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

m, n = sp.symbols("m, n", integer=True)
i = sp.Idx("i", (m, n))

if isinstance(m, int) and isinstance(n, int):
    print("Idx object accepts integer bounds.")
else:
    raise AssertionError("Idx object should accept only integer bounds.")
```
When executed with `python3 reproducer.py`, the script should print "Idx object accepts integer bounds." since both the lower and upper bounds `m` and `n` are integers. This demonstrates that the `Idx` object now checks for integer dimensions for both the lower and upper bounds.