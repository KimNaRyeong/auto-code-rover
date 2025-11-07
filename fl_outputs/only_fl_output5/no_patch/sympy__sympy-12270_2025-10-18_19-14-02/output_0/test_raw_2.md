Certainly! Based on the provided details regarding the expectation of the `.extract_multiplicatively()` method and the desired error output upon encountering an issue, I've structured a Python script named `reproducer.py`. This script aims to mimic the conditions under which the issue occurs and leverages your provided function to print a stack trace for any exceptions that align with a failure to meet the assertion criteria expected during the issue reproduction.

```python
import sympy as sp

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
    test_cases = [
        ((2+4*sp.I).extract_multiplicatively(2), 1 + 2*sp.I),
        ((-2-4*sp.I).extract_multiplicatively(-1), 2 + 4*sp.I),
        ((-2-4*sp.I).extract_multiplicatively(-2), None),
        ((2*sp.symbols('x') + 4*sp.symbols('y') + 8).extract_multiplicatively(2), sp.symbols('x') + 2*sp.symbols('y') + 4),
        ((-2*sp.symbols('x') - 4*sp.symbols('y') - 8).extract_multiplicatively(2), -sp.symbols('x') - 2*sp.symbols('y') - 4),
        ((-2*sp.symbols('x') - 4*sp.symbols('y') - 8).extract_multiplicatively(-1), 2*sp.symbols('x') + 4*sp.symbols('y') + 8),
        ((-2*sp.symbols('x') - 4*sp.symbols('y') - 8).extract_multiplicatively(-2), None)
    ]

    for i, (result, expected) in enumerate(test_cases, start=1):
        try:
            assert result == expected, f"Test case {i} failed. Expected {expected}, got {result}"
        except AssertionError as e:
            print_stacktrace(e)
            break
    else:
        print("No issues detected. All test cases passed.")

if __name__ == "__main__":
    main()
```

This script iterates through a series of predefined test cases that align with the scenarios described in the issue report. It compares the results of the `.extract_multiplicatively()` method against expected outcomes to confirm correctness. 

- For the test cases that should return a modified expression or `None` when a certain condition isn't met, assertions ensure these expectations are upheld.
- If an `AssertionError` is encountered, indicative of an inconsistency with the expected outcome, the script leverages the provided `print_stacktrace` function to display detailed information about the error context before terminating the loop.
- If all test cases pass without issue, it prints a confirmation message indicating no issues were detected, aligning with the script's requirements to exit with code 0 when the issue is fixed or is nonexistent based on the script's criteria.

Please ensure you have SymPy installed in your environment where you intend to run this script, as it is required for the calculations and assertions performed within.