import decimal

def test_approx_decimal():
    actual = [decimal.Decimal("1.000001"), decimal.Decimal("2.000001")]
    expected = [decimal.Decimal("1"), decimal.Decimal("2")]

    assert actual == pytest.approx(expected)

print_stacktrace(AssertionError)
