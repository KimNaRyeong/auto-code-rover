```python
from sympy import Rational
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

def main():
    try:
        # This should represent the number 0.5/100 accurately
        rational_from_strings = Rational('0.5', '100')
        # This is another way to represent 0.5/100, which is expected to give the same result
        rational_from_float_int = Rational(0.5, 100)
        
        # We assert that both representations should evaluate to the same value
        assert rational_from_strings == rational_from_float_int, \
            f"Mismatch: from strings: {rational_from_strings}, from float and int: {rational_from_float_int}"
       
        # If the issue is present, this line will not be reached
        print("Rational calculation is correct.")
        
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```