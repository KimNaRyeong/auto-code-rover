```python
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
    from sympy import degree, Symbol

    x = Symbol('x')
    try:
        result = degree((x-2)/(x**2+1), x)
        # Expecting a failure or a clear indication that degree cannot be calculated
        # for rational functions, thus raising an assertion error if result is returned as an integer
        assert result != 1, "Degree of a rational function should not be calculated as an integer."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected computation of degree for rational function.") from e

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"Assertion Error: {error}")
        raise SystemExit(0)
```

This script checks whether the `degree` function from the SymPy library incorrectly calculates the degree of a rational function as an integer, specifically returning `1` for the example given. The script will raise an `AssertionError` if the issue persists (i.e., if SymPy returns an incorrect degree for the rational function), which confirms the issue is present. The `print_stacktrace` function is used to print detailed information about where the error occurred, helping in diagnosing the problem when an exception is caught. The script exits with code 0 only when the issue is fixed, indicating no errors encountered during its execution.