 Here is a standalone Python script that reproduces the issue:
```python
from sympy import MatrixSymbol, I, S
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
When executed with `python3 reproducer.py`, it should print the following stack trace:
```vbnet
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
The script uses the `MatrixSymbol` function from the `sympy` library to create a 2x2 matrix symbol `M`. It then tries to print the product of `I` (the imaginary unit) and `M`, which raises a `TypeError` due to an invalid comparison of non-real numbers. The `print_stacktrace` function is used to print the stack trace of the error.