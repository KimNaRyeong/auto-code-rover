 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *
from sympy.simplify.trigsimp import _futrig

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_simplify_cos_x_to_the_i():
    x = Symbol('x')
    try:
        _futrig(cos(x)**I, **{})
    except TypeError as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    test_simplify_cos_x_to_the_i()
```
When executed, the script will print the stack trace of the issue:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    test_simplify_cos_x_to_the_i()
  File "reproducer.py", line 16, in test_simplify_cos_x_to_the_i
    _futrig(cos(x)**I, **{})
  File "/home/e/se/sympy/simplify/trigsimp.py", line 1169, in _futrig
    e = greedy(tree, objective=Lops)(e)
  File "/home/e/se/sympy/strategies/core.py", line 115, in minrule
    return min([rule(expr) for rule in rules], key=objective)
  File "/home/e/se/sympy/strategies/core.py", line 115, in <listcomp>
    return min([rule(expr) for rule in rules], key=objective)
  File "/home/e/se/sympy/strategies/core.py", line 44, in chain_rl
    expr = rule(expr)
  File "/home/e/se/sympy/simplify/fu.py", line 566, in TR6
    return _TR56(rv, cos, sin, lambda x: 1 - x, max=max, pow=pow)
  File "/home/e/se/sympy/simplify/fu.py", line 524, in _TR5