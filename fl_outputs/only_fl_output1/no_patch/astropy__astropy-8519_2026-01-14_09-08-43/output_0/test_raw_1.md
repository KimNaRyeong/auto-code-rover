Given your instructions and the requirement for handling errors properly in the Python script, I've revised the code. Considering the previous output, I'll avoid using numpy as it was not essential to reproduce the issue. Here is the standalone `reproducer.py` file designed to replicate the reported problem, handle the errors, and adhere to the guidelines provided for printing the stack trace.

```python
# reproducer.py
import astropy.units as u

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

def reproduce_issue(operation):
    color = 10*u.ABmag
    flux = 10000
    fluxMag = (flux*u.nJy).to(u.ABmag)
    try:
        if operation == "subtract":
            diff = fluxMag - color
            # Attempt to convert the result which is expected to fail if the issue exists.
            result = diff.to(u.nJy)
            print(color, fluxMag, diff, result)
        elif operation == "add":
            summ = fluxMag + color
            # Attempt to convert the result which is expected to fail if the issue exists.
            result = summ.to(u.nJy)
            print(color, fluxMag, summ, result)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError(f"Error encountered during {operation}.")

if __name__ == "__main__":
    # Intentionally separate the cases to clearly demonstrate which operation causes the issue.
    try:
        reproduce_issue("subtract")
    except AssertionError:
        pass  # Handle the first issue to allow testing the addition case.
    
    reproduce_issue("add")
```

This code should both reproduce the subtraction and addition issues as described, adhering to your requirements. It outputs detailed error information via `print_stacktrace` and raises an `AssertionError` if the operation leads to an exception, which aligns with the given scenario expectation.