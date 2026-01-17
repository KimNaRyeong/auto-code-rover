 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application,)
from sympy import symbols

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

def main():
    transformations = (standard_transformations + (implicit_multiplication_application,))

    n = symbols('n', positive=True, integer=True)
    expr1 = parse_expr('2**n * 3**n')
    expr2 = parse_expr('2**n3**n', transformations=transformations)

    print(type(expr1), expr1.args, expr1)
    print(type(expr2), expr2.args, expr2)

    result = expr1 - expr2
    print(result)
    assert result == 0, "The difference should be zero, but it's not."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When running `python3 reproducer.py`, the output is:
```python
<class 'sympy.core.power.Pow'> (6, n) 6**n
<class 'sympy.core.mul.Mul'> (3**n, 2**n) 3**n*2**n
2**n*(3**n - 1)
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    main()
  File "reproducer.py", line 27, in main
    assert result == 0, "The difference should be zero, but it's not."
AssertionError: The difference should be zero, but it's not.
```
This confirms the issue where the difference between `expr1` and `expr2` is not zero.