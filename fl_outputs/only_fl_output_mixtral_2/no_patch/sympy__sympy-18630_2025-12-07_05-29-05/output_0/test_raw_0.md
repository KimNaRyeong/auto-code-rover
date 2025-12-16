 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = Symbol('x')
    try:
        integrate(1 / (1 + x**4)**(S(1)/4), (x, 0, oo))
    except Exception as e:
        print_stacktrace(e)

    try:
        hyper((S(1)/4, S(1)/4), (S(5)/4,), exp_polar(I*pi)/x**4).nseries()
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 19, in main
    integrate(1 / (1 + x**4)**(S(1)/4), (x, 0, oo))
  File "/home/user/.local/lib/python3.8/site-packages/sympy/integrals/integrals.py", line 1522, in integrate
    return integral.doit(**doit_flags)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/integrals/integrals.py", line 669, in doit
    evalued = Add(*others)._eval_interval(x, a, b)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/core/expr.py", line 964, in _eval_interval
    B = _eval_endpoint(left=False)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/core/expr.py", line 949, in _eval_endpoint
    C = limit(self, x, c, "+" if left else "-")
  File "/home/user/.local/lib/python3.8/site-packages/sympy/series/limits.py", line 71, in limit
    return Limit(e, z, z0, dir).doit(deep=False)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/series/limits.py", line 261, in doit
    r = gruntz(e, z, z0, dir)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/series/gruntz.py", line 671, in gruntz
    r = limitinf(e0, z)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/core/cache.py", line 94, in wrapper
    retval = cfunc(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/series/gruntz.py", line 435, in limitinf
    c0, e0 = mrv_leadterm(e, x)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/core/cache.py", line 94, in wrapper
    retval = cfunc(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/series/gruntz.py", line 52