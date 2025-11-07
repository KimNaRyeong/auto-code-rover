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
        assert isinstance(p, sp.series.formal.FormalPowerSeries), "sympy.fps doesn't always return a formal power series"
        print("Issue not present")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will run the code that reproduces the issue, and if the issue is present, it will print a stack trace. If the issue is not present (i.e., the fix has been applied), it will print "Issue not present" and exit with code 0.