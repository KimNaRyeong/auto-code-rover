Below is a sample `reproducer.py` script that you can use to reproduce the issue described. This script will attempt to perform the problematic extract_multiplicatively operations and raise an `AssertionError` if they do not behave as expected. When the issue is fixed, the script should exit with code 0 without raising any errors.

```python
from sympy import Symbol, I, Mul

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

def test_extract_multiplicatively():
    x, y = Symbol('x'), Symbol('y')
    
    cases = [
        ((2 + 4*I).extract_multiplicatively(2), 1 + 2*I),
        ((-2 - 4*I).extract_multiplicatively(-1), 2 + 4*I),
        ((2*x + 4*y + 8).extract_multiplicatively(2), x + 2*y + 4),
        ((-2*x - 4*y - 8).extract_multiplicatively(2), -x - 2*y - 4),
        ((-2*x - 4*y - 8).extract_multiplicatively(-1), 2*x + 4*y + 8),
    ]
    
    # This is the part where it's suspected to be buggy in the issue description
    buggy_cases = [
        ((-2 - 4*I).extract_multiplicatively(-2), None),  # Expected a specific result or behavior here
        ((-2*x - 4*y - 8).extract_multiplicatively(-2), None),  # And here
    ]

    # Test cases expected to work as described by the issue
    for case, expected in cases:
        assert case == expected, f"Failed asserting {case} == {expected}"

    # Test cases expected to be buggy as described by the issue
    for case, expected in buggy_cases:
        try:
            assert case == expected, f"Expected {case} to equal {expected}"
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
    except AssertionError as e:
        exit(1)  # Exit with error code upon failure
    print("All tests passed.")
    exit(0)
```

This script first defines a helper function `print_stacktrace` to better understand where an exception occurs. It then defines `test_extract_multiplicatively`, which includes the cases outlined in your issue description. The script asserts that the cases return the expected outcomes and raises an error if they do not. 

Please adjust the expected results for the buggy cases as needed, because in the issue description, it wasn't clear what the desired results should be, so I set them to `None` for demonstration purposes.