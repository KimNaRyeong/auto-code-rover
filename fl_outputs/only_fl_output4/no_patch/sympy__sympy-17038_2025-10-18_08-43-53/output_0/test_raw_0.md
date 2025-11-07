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

def test_isqrt():
    from sympy.core.power import isqrt
    try:
        n1 = 4503599761588224
        expected_result1 = 67108864
        result1 = isqrt(n1)
        assert result1 == expected_result1, f"isqrt({n1}) = {result1}, expected {expected_result1}"

        n2 = 9999999999999999
        expected_result2 = 99999999
        result2 = isqrt(n2)
        assert result2 == expected_result2, f"isqrt({n2}) = {result2}, expected {expected_result2}"

        # This block won't be executed if the assertions fail
        print("All tests passed successfully. No issue found.")

    except AssertionError as e:
        print_stacktrace(e)
        raise # This will exit the script with a non-zero status due to the assertion error

if __name__ == "__main__":
    test_isqrt()
```