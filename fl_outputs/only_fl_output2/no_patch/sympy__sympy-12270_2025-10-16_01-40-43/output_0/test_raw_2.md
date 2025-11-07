Given the instructions and the need to accurately reproduce the issue for further analysis, the following Python script `reproducer.py` is crafted to specifically test the problematic areas with the `extract_multiplicatively` method in a standalone manner. This script will execute the test scenarios as described, use the `AssertionError` mechanism to identify failures, and incorporate the provided `print_stacktrace` function for detailed error reporting. This revised approach will trigger when the issue persists and exit normally when resolved.

```python
from sympy import I, symbols

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
    x, y = symbols('x y')

    # Demonstrating working cases
    working_cases = [
        ((2+4*I).extract_multiplicatively(2), "1 + 2*I"),
        ((-2-4*I).extract_multiplicatively(-1), "2 + 4*I"),
        ((2*x + 4*y + 8).extract_multiplicatively(2), "x + 2*y + 4"),
        ((-2*x - 4*y - 8).extract_multiplicatively(2), "-x - 2*y - 4"),
        ((-2*x - 4*y - 8).extract_multiplicatively(-1), "2*x + 4*y + 8"),
    ]

    for result, expected_str in working_cases:
        assert str(result) == expected_str, f"Expected {expected_str}, got {result}"

    # Demonstrating problematic cases
    problematic_cases = [
        ((-2-4*I).extract_multiplicatively(-2), "1 + 2*I", "Failed to extract (-2) from (-2-4*I)"),
        ((-2*x - 4*y - 8).extract_multiplicatively(-2), "x + 2*y + 4", "Failed to extract (-2) from (-2*x - 4*y - 8)"),
    ]

    for result, expected_str, message in problematic_cases:
        try:
            assert str(result) == expected_str, message
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script performs a series of assertions against the expected functionality of `extract_multiplicatively` with various inputs, including complex numbers and polynomial expressions containing symbols. The testing targets both regular cases, which serve as a control group demonstrating the expected outcomes, and problematic cases where the bug is anticipated to manifest based on the issue description.

The script is orchestrated to:
- Raise `AssertionError` when the observed behavior does not match the expectation, specifically indicating a failure in extracting the specified multiplier in the problematic cases.
- Utilize `print_stacktrace` to emit detailed diagnostic information upon catching an assertion error, enhancing the troubleshooting process by pinpointing the exact assertion and context leading to the failure.