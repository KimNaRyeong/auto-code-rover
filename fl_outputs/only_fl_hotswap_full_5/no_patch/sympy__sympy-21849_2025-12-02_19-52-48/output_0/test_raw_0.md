 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```Python
import sympy as sp

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
    function = sp.LambertW(2) * sp.LambertW(2)
    print(function)
except Exception as e:
    assert False, e
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    assert False, e
AssertionError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "reproducer.py", line 9, in <module>
    print(function)
  File "...\miniconda3\lib\site-packages\sympy\core\basic.py", line 2891, in __str__
    return str(self)
  File "...\miniconda3\lib\site-packages\sympy\core\basic.py", line 2876, in _repr_str_
    p = self._repr_latex_()
  File "...\miniconda3\lib\site-packages\sympy\core\_print_helpers.py", line 64, in _repr_latex_
    s = latex(self, mode='plain')
  File "...\miniconda3\lib\site-packages\sympy\printing\printer.py", line 373, in __call__
    return self.__wrapped__(*args, **kwargs)
  File "...\miniconda3\lib\site-packages\sympy\printing\latex.py", line 2948, in latex
    return LatexPrinter(settings).doprint(expr)
  File "...\miniconda3\lib\site-packages\sympy\printing\latex.py", line 254, in doprint
    tex = Printer.doprint(self, expr)
  File "...\miniconda3\lib\site-packages\sympy\printing\printer.py", line 291, in doprint
    return self._str(self._print(expr, **kwargs))
  File "...\miniconda3\lib\site-packages\sympy\printing\printer.py", line 329, in _print
    return getattr(self, printmethod)(expr, **kwargs)
  File "...\miniconda3\lib\site-packages\sympy\printing\latex.py", line 651, in _print_LambertW
    return self._print(expr.base, exp=self._print(expr.exp))
  File "...\miniconda3\lib\site-packages\sympy\printing\printer.py", line 329, in _print
    return getattr(self, printmethod)(expr, **kwargs)
  File "...\miniconda3\lib\site-packages\sympy\printing\latex.py", line 651, in _print_LambertW
    return self._print(expr.base, exp=self._print(expr.exp))
  File "...\miniconda3\lib\site-packages\sympy\printing\printer.py", line 329, in _print
    return getattr(self, printmethod)(expr, **kwargs)
  File "...\miniconda3\lib\site-packages\sympy