 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import sympify, RecursionError, I, oo

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
    g = oo
    expr = sympify("cosh(acos(-I + acosh(-g + I)))")
    try:
        result = expr.is_zero
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "RecursionError should not occur"
    else:
        assert result is not None, "Result should not be None"
```
When executed with `python3 reproducer.py`, the script should print the following stack trace and exit with code 1:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13
    result = expr.is_zero
