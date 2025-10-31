Here is the reproducer script:

```python
import sympy as sp
from sympy import Symbol, fps
import sys
import traceback

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = Symbol('x')
    p = fps(x ** 2)
    try:
        assert isinstance(p, sp.series.formal.FormalPowerSeries), "p is not a formal power series"
        if p[0]:
            raise AssertionError("sympy.fps doesn't always return a formal power series")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present, and it will print the stack trace. If the issue is fixed, it will exit with code 0.