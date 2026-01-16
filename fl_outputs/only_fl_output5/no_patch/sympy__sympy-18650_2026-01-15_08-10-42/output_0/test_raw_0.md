```python
# reproducer.py

from sympy import sqrt, Rational

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

def test_sqrt_rational():
    try:
        result = sqrt(8)**Rational(2, 3)
        expected_result = 2

        # Simplify the result to check if equivalent to expected result
        simplified_result = result.simplify()

        # Use .equals() for mathematical comparison instead of == to compare symbolic expressions
        assert simplified_result.equals(expected_result), f"Result {simplified_result} is not equal to {expected_result}"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_sqrt_rational()
```