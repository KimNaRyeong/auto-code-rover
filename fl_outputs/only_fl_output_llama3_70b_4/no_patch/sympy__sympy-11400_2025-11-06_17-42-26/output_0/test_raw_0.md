Here is the `reproducer.py` file that reproduces the issue:
```
from sympy import symbols, sinc, ccode
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')

try:
    result = ccode(sinc(x))
    assert 'sin(x)/x' in result, "ccode(sinc(x)) does not work as expected"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
```
This script defines a symbol `x` and tries to generate C code for the sinc function using `ccode`. If the generated code does not contain the string `'sin(x)/x'`, it raises an `AssertionError` with a message indicating that the issue is present. The `print_stacktrace` function is used to print the stack trace of the error, including line numbers and code context. If the issue is fixed, the script prints a success message and exits with code 0.