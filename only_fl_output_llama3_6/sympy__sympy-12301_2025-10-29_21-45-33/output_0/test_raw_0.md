Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import sympy
from sympy import init_printing

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
    try:
        os.environ['PYTHONHASHSEED'] = '736538842'
        sympy.init_printing(use_latex=False)
        sympy.test(split='4/4', seed=57601301)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the environment variable `PYTHONHASHSEED` to the specified value, initializes SymPy with LaTeX rendering disabled, and then runs the test with the specified seed. If an `AssertionError` is raised during the execution of the test, it prints the stack trace using the provided function and re-raises the exception.

To reproduce the issue, simply run the script using Python 3: `python3 reproducer.py`. This should raise an `AssertionError` with a stack trace that includes the line numbers.