 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class A:
    @classmethod
    @property
    def f(cls):
        """Some class property."""
        return "property"

if __name__ == "__main__":
    # The following lines should raise AssertionError
    # if the issue is present, and print a stack trace.
    assert A.f.__doc__ == "Some class property.", "Documentation not found."
    print("Documentation found.")

    # Exit with code 0 if the issue is fixed.
    sys.exit(0)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace. If the issue is fixed, the script should print "Documentation found." and exit with code 0.