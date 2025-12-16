 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import MatrixSymbol, I, Matrix

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        M = MatrixSymbol('M', 2, 2)
        print(I * M)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the issue and raise an `AssertionError` to indicate that the issue is present. The script will exit with a non-zero exit code.

If the issue is fixed, the script will not raise any exceptions and will exit with a zero exit code.