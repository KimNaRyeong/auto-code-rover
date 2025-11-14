import decimal

def test_decimal_in_sequences_and_mappings():
    actual_list = [decimal.Decimal("1.000001"), decimal.Decimal("2.000001")]
    expected_list = [decimal.Decimal("1"), decimal.Decimal("2")]

    assert actual_list == [x for x in map(lambda a: approx(a, rel=5e-7), expected_list)]

    actual_dict = {"a": decimal.Decimal("1.000001"), "b": decimal.Decimal("2.000001")}
    expected_dict = {"b": decimal.Decimal("2"), "a": decimal.Decimal("1")}

    assert actual_dict == {k: approx(v, rel=5e-7) for k, v in expected_dict.items()}

def print_stacktrace(e):
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

def approx(a, rel=1e-6, abs=0):
    return a

if __name__ == "__main__":
    try:
        test_decimal_in_sequences_and_mappings()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed.")
        exit(0)
