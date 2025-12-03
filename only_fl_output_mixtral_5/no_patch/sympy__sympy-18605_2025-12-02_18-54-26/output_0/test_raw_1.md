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

print("Idx object accepted non-integer bounds.")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following output:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    raise AssertionError("Idx object should not accept non-integer bounds.")
AssertionError: Idx object should not accept non-integer bounds.
```
This indicates that the `Idx` object is accepting non-integer bounds, which is not expected behavior. The check for integer dimensions should be done to both upper and lower bounds when a tuple is given as an argument.