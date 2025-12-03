 I apologize for the syntax error in my previous response. Here is the corrected `reproducer.py` file:
```python
from sympy import convert_to, kg, m, s, joule
import sys, traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    J = kg*m**2/s**2
    try:
        result = convert_to(J*s, joule)
        assert result == J*s, "convert_to should return the original expression when the target unit is the same as the given unit."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("convert_to passes the test when the target unit is the same as the given unit.")

    try:
        result = convert_to(joule*second, joule)
        assert result == joule*second, "convert_to should return the original expression when the target unit is a multiple of the given unit."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("convert_to passes the test when the target unit is a multiple of the given unit.")

    try:
        result = convert_to(J*s, kg*m**2/s)
        assert result == J*s, "convert_to should return the original expression when the target unit is a factor of the given unit."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("convert_to passes the test when the target unit is a factor of the given unit.")

    try:
        result = convert_to(J*s, mins)
        assert result == J*mins/60, "convert_to should return the correct expression when the target unit is not a factor or multiple of the given unit."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("convert_to passes the test when the target unit is not a factor or multiple of the given unit.")

    print("All tests pass.")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace if the issue is present, and print "All tests pass." if the issue is fixed.