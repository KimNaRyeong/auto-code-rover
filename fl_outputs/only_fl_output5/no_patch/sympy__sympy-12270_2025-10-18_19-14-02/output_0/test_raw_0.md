Below is a `reproducer.py` python script that will attempt to reproduce the issue as described. It utilizes `sympy`, a Python library for symbolic mathematics to check the behavior of `.extract_multiplicatively()` function for various scenarios, including the potential bug situations. It asserts the expected outcomes, raising an `AssertionError` if the behavior does not match expected results, providing a detailed stack trace for debugging purposes.

```python
import sympy as sp

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

def check_extract_multiplicatively():
    # First set of tests as mentioned
    try:
        assert (2+4*sp.I).extract_multiplicatively(2) == 1 + 2*sp.I
        assert (-2-4*sp.I).extract_multiplicatively(-1) == 2 + 4*sp.I
        assert (-2-4*sp.I).extract_multiplicatively(-2) == None, "Potential Bug Detected!"
    except AssertionError as e:
        print("Issue detected in complex number tests.")
        print_stacktrace(e)
        exit(1)

    # Second set of tests with symbols
    x, y = sp.symbols('x y')
    try:
        assert (2*x + 4*y + 8).extract_multiplicatively(2) == x + 2*y + 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(2) == -x - 2*y - 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(-1) == 2*x + 4*y + 8
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert result == None, f"Expected None, found {result}. Potential Bug Detected!"
    except AssertionError as e:
        print("Issue detected in symbolic expression tests.")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    check_extract_multiplicatively()
    print("No issues detected.")
```

This script checks both the scenarios involving simple complex number manipulations as well as symbolic expressions. If the library behaves as expected and fixes the issues identified, this script should exit with code 0 and print "No issues detected." If the issue exists, it will raise an `AssertionError` detailing the problematic assertion, and print a detailed stack trace for debugging purposes.