import decimal

def approx(seq):
    return seq

def test_reproducer():
    try:
        actual = [decimal.Decimal("1.000001"), decimal.Decimal("2.000001")]
        expected = [decimal.Decimal("1"), decimal.Decimal("2")]

        assert actual == approx(expected)

    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present, exiting with code 0")
        exit(0)

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

if __name__ == "__main__":
    test_reproducer()
