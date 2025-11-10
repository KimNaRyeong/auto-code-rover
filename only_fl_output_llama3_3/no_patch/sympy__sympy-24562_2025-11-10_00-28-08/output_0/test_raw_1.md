Here is the reproducer script:

```python
import sympy
from sys import exit, stderr

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=stderr)
        print(f"    {line_number}: {code_context}", file=stderr)
    print(f"{e.__class__.__name__}: {e}", file=stderr)

try:
    rational1 = sympy.Rational('0.5', '100')
    rational2 = sympy.Rational(0.5, 100)
    assert rational1 == rational2
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not reproduced")
    exit(0)
```

This script creates two `Rational` objects with the same value but different representations and checks if they are equal. If the assertion fails, it prints the stack trace and exits with code 1. If the assertion succeeds, it prints a message indicating that the issue was not reproduced and exits with code 0.