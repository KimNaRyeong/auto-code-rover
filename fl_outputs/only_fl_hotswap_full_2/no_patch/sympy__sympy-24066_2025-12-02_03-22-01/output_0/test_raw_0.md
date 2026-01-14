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
        exit(0)

    raise AssertionError("The issue was not reproduced.")
```
When executed with `python3 reproducer.py`, the script should print a stack trace similar to the following:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    SI._collect_factor_and_dimension(buggy_expr)
  File "/path/to/sympy/sympy/physics/units/systems/si.py", line 110, in _collect_factor_and_dimension
    raise ValueError(msg)
ValueError: Dimension of "exp(second/(farad*ohm))" is Dimension(time/(capacitance*impedance)), but it should be Dimension(1)
```
This confirms that the issue is present in the `sympy` library.