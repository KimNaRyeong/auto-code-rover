 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import exp, S
from sympy.physics import units
from sympy.physics.units.systems.si import SI

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
    expr = units.second / (units.ohm * units.farad)
    dim = SI._collect_factor_and_dimension(expr)[1]

    assert SI.get_dimension_system().is_dimensionless(dim)

    buggy_expr = 100 + exp(S(expr))
    try:
        SI._collect_factor_and_dimension(buggy_expr)
    except ValueError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script raises a `ValueError` with a stack trace, which indicates that the issue is present. The line numbers in the stack trace may differ depending on the version of Sympy and the environment in which the script is executed.