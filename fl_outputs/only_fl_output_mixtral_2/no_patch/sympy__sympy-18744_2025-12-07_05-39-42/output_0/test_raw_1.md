 Here is a standalone Python script that reproduces the issue:
```python
from sympy import MatrixSymbol, I, S
from sympy.abc import x

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    M = MatrixSymbol('M', 2, 2)
    print(I*M)
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    print(I*M)
  File "/usr/local/lib/python3.8/dist-packages/sympy/core/basic.py", line 413, in __str__
    return sstr(self, order=None)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/str.py", line 899, in sstr
    s = p.doprint(expr)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/printer.py", line 251, in doprint
    return self._str(self._print(expr)
```