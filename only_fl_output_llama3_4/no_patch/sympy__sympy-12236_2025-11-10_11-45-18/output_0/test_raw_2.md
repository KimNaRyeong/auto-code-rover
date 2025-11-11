Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy
from sympy import symbols

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

def reproduce_issue():
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)
    
    try:
        bug.apart()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Wrong result with apart")

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function, which creates the expressions and tries to simplify them using `apart()`. If an exception is raised during this process (which should be a `NotImplementedError`), it prints the stack trace of the issue and raises an `AssertionError`.