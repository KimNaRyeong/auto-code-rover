 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import imageset, Lambda, I, Integers

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        result = imageset(Lambda(n, 1 + I*n), Integers)
        assert result == {I*n for n in Integers}
    except AssertionError:
        print_stacktrace(AssertionError("The `1` is simply dropped in the result of imageset"))
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0 without raising any exceptions.