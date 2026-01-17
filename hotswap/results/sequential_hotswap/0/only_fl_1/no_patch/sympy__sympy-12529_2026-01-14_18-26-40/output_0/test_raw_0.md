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

def test_totient_non_integer():
    from sympy import totient

    try:
        result = totient(2.3)
        raise AssertionError("Totient function did not raise an error for non-integer input.")
    except ValueError as ve:
        print("Test passed: ValueError raised as expected for non-integer input.")
    except Exception as e:
        print("Unexpected error encountered.")
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        test_totient_non_integer()
    except AssertionError as ae:
        print_stacktrace(ae)
        exit(1)  # Exit with an error code if the assertion fails
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("No issues detected.")
        exit(0)  # Exit with a success code if no issues were detected
```