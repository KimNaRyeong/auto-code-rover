from decimal import Decimal
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

def test_decimal_in_sequences_and_mappings():
    actual = [Decimal("1.000001"), Decimal("2.000001")]
    expected = [Decimal("1"), Decimal("2")]

    try:
        assert actual == [x for x in expected]
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_decimal_in_sequences_and_mappings()
