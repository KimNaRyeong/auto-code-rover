Here's a standalone Python file named `reproducer.py` that matches your specifications for reproducing the issue:

```python
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
    from django.core.validators import DecimalValidator
    from django.core.exceptions import ValidationError
    from decimal import Decimal
    try:
        value = '0E+1'
        validator = DecimalValidator(max_digits=8, decimal_places=7)
        validator(Decimal(value))
        # If it reaches this point, no ValidationError was raised for the problematic value
        print("The issue is fixed. Exiting with code 0.")
    except ValidationError as e:
        print_stacktrace(e)
        assert False, f"'{value}' should be a valid decimal but raised ValidationError."

if __name__ == "__main__":
    main()
```

When you run `python3 reproducer.py` in the root directory of your project, this script will execute the test case provided. 

- If the issue is present (i.e., `0E+1` is not treated as a valid decimal by the `DecimalValidator` in your current Django version), the script will catch a `ValidationError`, print the stack trace of this issue clearly indicating where the failure occurred, and raise an `AssertionError`.
- If the problem has been fixed in your Django environment (i.e., `0E+1` is correctly recognized as a valid decimal and does not raise a `ValidationError`), the script will print "The issue is fixed. Exiting with code 0." and exit normally with code `0`. 

Please ensure that Django is correctly installed and configured in your Python environment where this script will be executed.