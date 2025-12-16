 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy.solvers.decompogen import decompogen
from sympy.abc import x
from sympy import Min

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
    decompogen(Min(5, x), x)
except Exception as e:
    print_stacktrace(e)
    assert False, "An exception should not be raised"
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    assert False, "An exception should not be raised"
AssertionError: An exception should not be raised
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    decompogen(Min(5, x), x)
  File "sympy\solvers\decompogen.py", line 57, in decompogen
    result += [f1] + decompogen(f2, symbol)
  File "sympy\solvers\decompogen.py", line 57, in decompogen
    result += [f1] + decompogen(f2, symbol)
  File "sympy\solvers\decompogen.py", line 57, in decompogen
    result += [f1] + decompogen(f2, symbol)
  File "sympy\solvers\decompogen.py", line 51, in decompogen
    fp = Poly(f)
  File "sympy\polys\polytools.py", line 128, in __new__
    return cls._from_expr(rep, opt)
  File "sympy\polys\polytools.py", line 238, in _from_expr
    rep, opt = _dict_from_expr(expr, opt)
  File "sympy\polys\polyutils.py", line 367, in _dict_from_expr
    rep, gens = _dict_from_expr_no_gens(expr, opt)
  File "sympy\polys\polyutils.py", line 310, in _dict_from_expr_no_gens
    (poly,), gens = _parallel_dict_from_expr_no_gens((expr,), opt)
  File "sympy\polys\polyutils.py", line 273, in _parallel_dict_from_expr_no_gens
    gens = _sort_gens(gens, opt=opt)
  File "sympy\polys\polyutils.py", line 106, in _sort_gens
    gens = sorted(gens, key=order_key)
  File "sympy\polys\polyutils.py", line 78, in order_key
    gen = str(gen)
  File "sympy\core\basic.py", line 400, in __str__
    return sstr(self, order=None)
  File "sympy\printing\str.py", line 796, in sstr
    s = p.doprint(expr)
  File "sympy\printing\printer.py", line 233, in doprint
    return self._str(self._print(expr))
  File "sympy\printing\printer.py", line 257, in _print
    return getattr(self, printmethod)(expr, *args, **kwargs)
  File "sympy\printing\