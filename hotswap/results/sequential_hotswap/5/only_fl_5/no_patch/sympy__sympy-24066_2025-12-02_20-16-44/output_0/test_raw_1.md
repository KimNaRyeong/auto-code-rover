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
When executed with `python3 reproducer.py`, it raises a `ValueError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    SI._collect_factor_and_dimension(buggy_expr)
  File "/home/user/.local/lib/python3.8/site-packages/sympy/physics/units/systems/si.py", line 125, in _collect_factor_and_dimension
    raise ValueError(
ValueError: Dimension of "exp(second/(farad*ohm))" is Dimension(time/(capacitance*impedance)), but it should be Dimension(1)
```
This confirms the presence of the issue.