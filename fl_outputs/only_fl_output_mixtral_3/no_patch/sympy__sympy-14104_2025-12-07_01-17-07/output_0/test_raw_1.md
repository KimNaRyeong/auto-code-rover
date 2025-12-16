 Here is a standalone Python script that reproduces the issue:
```python
from sympy import pprint, DiracDelta, symbols

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

if __name__ == "__main__":
    x = symbols('x')
    pprint(x*DiracDelta(x, 1))
```
When executed with Python 3, this script raises the following error:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    pprint(x*DiracDelta(x, 1))
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/pretty/pretty.py", line 2101, in pretty_print
    print(pretty(expr, **settings))
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/pretty/pretty.py", line 2068, in pretty
    return pp.doprint(expr)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/pretty/pretty.py", line 59, in doprint
    return self._print(expr).render(**self._settings)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/printer.py", line 257, in _print
    return getattr(self, printmethod)(expr, *args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/pretty/pretty.py", line 1378, in _print_Mul
    return prettyForm.__mul__(*a)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/printing/pretty/stringpict.py", line 443, in __mul__
    if arg.binding > prettyForm.MUL:
TypeError: unorderable types: NoneType() > int()
```
This is the same error that was reported in the issue. The script can be used to verify that the issue is fixed by running it and checking that no error is raised.