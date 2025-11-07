import sys
from unittest.mock import Mock

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

# Mocking Django's behavior for demonstration purposes
def prepare_lookup_value(key, value):
    """
    Mocked implementation for preparing lookup value.
    Trying to replicate the splitting logic that fails with comma-containing values.
    """
    if key.endswith('__in'):
        return value.split(',')
    return value

def test_comma_inclusion():
    try:
        values = prepare_lookup_value('username__in', 'john,doe,jane,roe')
        assert 'john,doe' in values, "Value with comma not correctly included."
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        test_comma_inclusion()
    except AssertionError:
        sys.exit(1)
    else:
        print("No issue found or issue has been resolved.")
        sys.exit(0)
