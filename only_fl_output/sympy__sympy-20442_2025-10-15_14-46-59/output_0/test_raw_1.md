Below is the standalone Python file `reproducer.py` to reproduce the issue as described. The script is designed to trigger an `AssertionError` when the unusual behavior of `convert_to` from the `sympy` library (version 1.4 as specified) is observed, indicating the presence of the reported issue. When the issue is fixed in a future release of `sympy`, the script should exit with code 0, indicating no error.

```python
import sys
from sympy import symbols, convert_to, joule, s

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

def test_convert_to_issue():
    # Define units
    kg, m = symbols('kg m')
    J = kg * m ** 2 / s ** 2
    # Test if convert_to behaves as reported
    try:
        result = convert_to(joule * s, joule)
        # Check for expected result
        assert result != joule**(7/9), "Unexpected conversion result."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code
    
    # If no exception occurs, print a success message
    print("Issue not present or has been fixed.")
    sys.exit(0)

if __name__ == "__main__":
    test_convert_to_issue()
```

This script attempts to convert joules per second to joules using the `sympy` library's `convert_to` function, expecting a certain behavior as described in the issue. The precision of the conversion and the specific unexpected output (`joule**(7/9)`) are used as criteria to check whether the issue is present. The use of `assert` statement ensures that any deviation from the expected or corrected behavior is caught, and the script uses the `print_stacktrace` function to provide detailed error information before exiting.
