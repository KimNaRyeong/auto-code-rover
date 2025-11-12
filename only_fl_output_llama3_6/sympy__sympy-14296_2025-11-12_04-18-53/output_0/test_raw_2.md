Here is the standalone Python file `reproducer.py` to reproduce the issue:

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
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    if not (a.minpoly == sp.Poly([1, 0, -1])):
        raise AssertionError("Issue present")
    print_stacktrace(AssertionError("Issue fixed"))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will run the same code that reproduces the issue, and if the issue is present (i.e., the minimal polynomial of `a` is not correct), it will raise an `AssertionError`. If the issue is fixed, it will print a message indicating that the issue was fixed.