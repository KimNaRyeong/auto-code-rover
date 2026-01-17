import sys
import traceback
from decimal import Decimal, InvalidOperation
from django.db.backends.utils import format_number

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def format_number_with_quantize(value: Decimal, max_digits: int, decimal_places: int):
    try:
        return format_number(value, max_digits, decimal_places)
    except InvalidOperation:
        print_stacktrace(InvalidOperation("InvalidOperation occurred during quantization."))
        assert False, "InvalidOperation error raised during quantization."

def test_invalid_decimal_query():
    # Test value that should raise InvalidOperation error during quantization
    value = Decimal("12345.00")

    # Test with max_digits=4 and decimal_places=0
    max_digits = 4
    decimal_places = 0

    # Perform quantization and check for InvalidOperation error
    format_number_with_quantize(value, max_digits, decimal_places)

if __name__ == "__main__":
    try:
        test_invalid_decimal_query()
        print("Test passed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
