```python
# reproducer.py
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

    value = '0E+1'
    validator = DecimalValidator(8, 7)
    
    try:
        validator(Decimal(value))
    except ValidationError as e:
        print_stacktrace(e)
        raise AssertionError(f"Validation failed for '{value}'. Decimal in scientific notation should be considered valid.") from None

if __name__ == "__main__":
    main()
```