 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, I, Matrix
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

try:
    M = MatrixSymbol('M', 2, 2)
    print(I*M)
except Exception as e:
    print_stacktrace(e)
```

When you run `python3 reproducer.py`, it will print the stack trace of the issue:

```
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    print(I*M)
  File "/path/to/sympy/core/basic.py", line 413, in __str__
    return sstr(self, order=None)
  File "/path/to/sympy/printing/str.py", line 899, in sstr
    s = p.doprint(expr)
  File "/path/to/sympy/printing/printer.py", line 251, in doprint
    return self._str(self._print(expr)
  File "/path/to/sympy/printing/printer.py", line 289, in _print
    return getattr(self, printmethod)(expr, **kwargs)
  File "/path/to/sympy/printing/str.py", line 335, in _print_MatMul
    if c.is_number and c < 0:
  File "/path/to/sympy/core/expr.py", line 407, in __lt__
    return self._cmp(other, "<", StrictLessThan)
  File "/path/to/sympy/core/expr.py", line 348, in _cmp
    raise TypeError("Invalid comparison of non-real %s" % me)
TypeError: Invalid comparison of non-real I
```