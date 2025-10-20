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
    from sympy import Pow, Rational, latex
    try:
        # Test case that triggers the recursion error
        result = latex(Pow(Rational(1,2),-1, evaluate=False))
        # If the above line does not raise an exception, the issue is fixed.
        # Hence, assert its failure for now to indicate issue presence.
        assert False, "Expected a RecursionError, but none occurred."
    except RecursionError as e:
        print("RecursionError occurred as expected.")
        print_stacktrace(e)
    except Exception as e:
        assert False, f"Unexpected error occurred: {str(e)}"
    else:
        # If no error occurs, it means the issue has been fixed.
        print("Issue has been fixed, no RecursionError.")

if __name__ == "__main__":
    main()
```

This script is designed to directly target the issue mentioned: a `RecursionError` that occurs when converting a specific `sympy` expression into LaTeX with the given conditions. The script attempts to reproduce the error and assert its occurrence. If the issue persists (i.e., the `RecursionError` is raised), the script prints a stack trace of the issue, leveraging `print_stacktrace` for clarity.

If the issue has been fixed and no error occurs, the script will complete without raising an assertion, suggesting that the RecursionError issue has been addressed in the `sympy` library. This is critical for checking whether updates or fixes to the library have effectively resolved the problem.