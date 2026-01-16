```python
import astropy.units as u
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def perform_operations_and_assert():
    color = 10*u.ABmag
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)

    # Attempt subtraction operation
    diff = fluxMag - color
    # Check if the result of subtraction maintains ABmag unit
    try:
        assert diff.unit == u.ABmag, "Subtraction does not preserve ABmag unit."
    except AssertionError as e:
        print("AssertionError in subtraction operation.")
        raise

    # Attempt addition operation, which should also maintain the ABmag unit
    try:
        addition_result = fluxMag + color
        assert addition_result.unit == u.ABmag, "Addition does not preserve ABmag unit."
    except AssertionError as e:
        print("AssertionError in addition operation.")
        raise

def main():
    try:
        perform_operations_and_assert()
        print("No AssertionError. Unit operations preserve ABmag unit as expected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by performing both addition and subtraction operations with `ABmag` units and then asserting that the results of these operations still have `ABmag` units. The `AssertionError` should be raised if the operation does not maintain ABmag units, which reproduces the original issue. During normal operation, if the issue is present, running this script (`python3 reproducer.py`) will result in assertion errors that confirm the presence of the issue, accompanied by a printed stack trace for deeper investigation.